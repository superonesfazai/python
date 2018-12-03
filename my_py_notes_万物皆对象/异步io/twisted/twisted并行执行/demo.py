# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

from twisted.internet import reactor
from twisted.internet import defer
from twisted.internet import task

# Twisted has a slightly different approach
def schedule_install(customer):
    # They are calling us back when a Wordpress installation completes.
    # They connected the caller recognition system with our CRM and
    # we know exactly what a call is about and what has to be done next.
    # We now design processes of what has to happen on certain events.
    def schedule_install_wordpress():
        def on_done():
            print("Callback: Finished installation for", customer)

        print("Scheduling: Installation for", customer)

        return task.deferLater(reactor, 3, on_done)

    #
    def all_done(_):
        print("All done for", customer)
    #
    # For each customer, we schedule these processes on the CRM
    # and that
    # is all our chief-Twisted developer has to do
    d = schedule_install_wordpress()
    d.addCallback(all_done)

    return d

# 是的，我们不再需要很多开发人员，也不需要任何同步。
# ~~ Super-powered Twisted developer ~~
def twisted_developer_day(customers):
    print("Goodmorning from Twisted developer")
    # Here's what has to be done today
    work = [schedule_install(customer) for customer in customers]
    # Turn off the lights when done
    join = defer.DeferredList(work)
    join.addCallback(lambda _: reactor.stop())

    print("Bye from Twisted developer!")

# Even his day is particularly short!
twisted_developer_day(["Customer %d" % i for i in range(15)])
# Reactor, our secretary uses the CRM and follows-up on events!
reactor.run()

# 并且没有使用线程。我们并行地处理了15个消费者
# 这个窍门就是我们把所有的阻塞的对sleep()的调用都换成了Twisted中对等的task.deferLater()和回调函数。