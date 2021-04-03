########################################
#
#   非同期処理の為の基底クラス
#   と思ったけど、wxPythonと相性悪そうでやめた
#
########################################

import asyncio


class AsyncProcess:
    def __init__(self):
        self.thread_run = False
        self.thread_function = self.dummy

    async def dummy(self):
        await self.sleep(1)

    async def thread(self):
        print("thread 1")
        while self.thread_run:
            print("thread 2")
            if self.thread_function is not None:
                print("thread 3")
                await self.thread_function()
                print("thread 4")
        print("thread 5")

    async def sleep(self, sec):
        print("Sleep {0} sec".format(sec))
        await asyncio.sleep(sec)
        print("sleep 2")

    def start_thread(self):
        print("start_thread 1")
        self.thread_run = True
        asyncio.ensure_future(self.thread())
        ## self.task = asyncio.create_task(self.thread())
        print("start_thread 2")

    def stop_thread(self):
        self.thread_run = False
        print("stop_thread 2")


if __name__ == "__main__":
    async def sleeping(order, seconds, hook=None):
        await asyncio.sleep(seconds)
        if hook:
            hook(order)
        return order


    async def blink(count):
        for i in range(1, count):
            r = await sleeping("blink", 1)
        print("blink:complete")


    async def trigger(sec, obj):
        r = await sleeping("trigger", sec)
        print("trigger call {0}sec".format(sec))
        obj.stop_thread()

    def process(loop):
        print("process 1")
        obj = AsyncProcess()
        print("process 2")
        obj.start_thread()
        print("process 3")
        return obj

    loop = asyncio.get_event_loop()
    obj = process(loop)
    asyncio.ensure_future(trigger(7, obj))
    loop.run_until_complete(blink(15))

