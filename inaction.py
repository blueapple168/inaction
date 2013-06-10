#!/usr/bin/python
# coding=utf-8
import pyinotify
import os
import re
import logging

class Rule(object):
    '''A rule bind command to a pathname'''
    def __init__(self, pathname, events, command):
        self.pathname = pathname
        self.events = events
        self.command = command

    def execute(self):
        real_cmd = self.command % ({
            'pathname': self.pathname,
        })

        #如果命令以@开头, 则去掉@, 不输出命令.
        if real_cmd.startswith('@'):
            real_cmd = real_cmd[1:]
        else:
            print real_cmd

        os.system(real_cmd)

    def __repr__(self):
        return 'inaction.Rule("%s", %s, "%s")' % (self.pathname,
                                                  self.events,
                                                  self.command)

class Rules(dict):
    '''rules parsed from Inactionfile'''
    def __init__(self, acfile='Inactionfile'):
        def parse_line(l):
            l = re.sub('\s*#.*$', '', l)
            pathname,events,command = [ s.strip() for s in re.split('\s+', l, 2) ]

            pathname = os.path.realpath(pathname)
            events = [ pyinotify.EventsCodes.ALL_FLAGS.get(flag.strip())
                     for flag in events.split(',') ]

            if None in events:
                raise ConfigError

            self[pathname] = Rule(pathname, events, command)

        with open(acfile) as f:
            for l in f:
                if l.startswith('#'):
                    continue
                parse_line(l)

    def related_events(self):
        es = []
        for f,r in self.items():
            es += r.events
        return list(set(es))

class InActionHandler(pyinotify.ProcessEvent):
    def my_init(self):
        pass

    def set_rules(self, rules):
        self.rules = rules

    def process_default(self, event):
        event_pathname = os.path.realpath(event.pathname)
        rule = rules.get(event_pathname)
        if rule:
            for expected_event in rule.events:
                if event.mask & expected_event:
                    rule.execute()
                    logging.debug('Hit %s(mask %s,%s)' % (event_pathname,
                                                         event.maskname,
                                                         event.mask))
                    break

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage='...')

    parser.add_option("-r", "--recursive", action="store_true",
                      dest="recursive",
                      help="Add watches recursively on paths")
    parser.add_option("-a", "--auto_add", action="store_true",
                      dest="auto_add",
                      help="Automatically add watches on new directories")

    (options, args) = parser.parse_args()


    rules = Rules()
    mask = reduce(lambda x, y: x | y, rules.related_events())
    wm = pyinotify.WatchManager()

    wm.add_watch(args or '.', mask,
                 rec=options.recursive,
                 auto_add=options.auto_add,)

    handler = InActionHandler()
    handler.set_rules(rules)

    notifier = pyinotify.Notifier(wm, handler)
    notifier.loop()
