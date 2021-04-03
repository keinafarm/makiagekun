#################################
#   Pythonにおける非同期処理の習作
#   https://qiita.com/icoxfog417/items/07cbf5110ca82629aca0
#################################

import asyncio


Seconds = [
    ("first", 5),
    ("second", 0),
    ("third", 3)
]


async def sleeping(order, seconds, hook=None):
    await asyncio.sleep(seconds)
    if hook:
        hook(order)
    return order


async def basic_async(num):
    # the order of result is nonsequential (not depends on order, even sleeping time)
    print("basic_async:1")
    for s in Seconds:
        print("basic_async:2")
        r = await sleeping(*s)
        print("basic_async:3")
        print("{0}'s {1} is finished.".format(num, r))
    print("basic_async:4")

    return True

async def   alarm(sec):
    r = await sleeping("alarm", sec)
    print("Alarm timeout {0}sec".format(sec))

class prinout:
    def __init__(self):
        self.counter = 0
        self.status = False
    def out(self):
        self.counter += 1
        print("blink timeout {0}sec".format(self.counter))
    def check(self):
        return self.status
    def trigger(self):
        self.status = True

async def   blink(count, obj):
    func1 = sleeping
    for i in range(1,count):
        r = await func1("blink", 1)
        prn.out()
        if obj.check():
            print("blink:terminate")
            return
    print("blink:complete")

async def   trigger(sec, obj):
    r = await sleeping("trigger", sec)
    print("trigger call {0}sec".format(sec))
    obj.trigger()


if __name__ == "__main__":
    func = alarm
    loop = asyncio.get_event_loop()
    # make two tasks in event loop
    print("process1")
    asyncio.ensure_future(basic_async(1))
    print("process2")
    asyncio.ensure_future(basic_async(2))
    print("process3")
    asyncio.ensure_future(alarm(6))
    print("process4")
    prn = prinout()
    print("process5")
    asyncio.ensure_future(blink(10, prn))
    print("process6")
    asyncio.ensure_future(trigger(7, prn))
    print("process7")
    loop.run_until_complete(func(15))
    print("process8")

    # loop.run_forever()