###########################################
#
#   LIFOなLinkedList
#
###########################################
from ThreadBase import ThreadBase


class LinkedList:
    def __init__(self):
        """
        管理ポインタの初期化
        """
        ThreadBase.lock_init()

        self.head = None
        self.tail = None

    def append(self, obj):
        """
        リストの最後に追加
        :param obj: 追加するオブジェクト
        :return:
        """
        ThreadBase.lock()
        if self.tail is None:  # まだ何もLINKされていない
            obj.follow = None
            obj.prev = None
            self.head = obj
            self.tail = obj
        else:  # linkされている
            current_last = self.tail  # 最後に追加
            obj.prev = current_last
            obj.follow = None
            self.tail = obj
            current_last.follow = obj
        ThreadBase.unlock()

    def get_top(self):
        """
        リストの先頭から取得
        :return:
        """
        if self.head is None:  # なにもない
            return None
        else:
            ThreadBase.lock()
            current_top = self.head
            follow_top = current_top.follow
            if follow_top is None:  # 取り出したら無くなった
                self.head = None
                self.tail = None
                ThreadBase.unlock()
                return current_top
            else:
                self.head = follow_top
                follow_top.prev = None
                ThreadBase.unlock()
                return current_top

    def top(self):
        """
        先頭のオブジェクトを見る
        :return: 先頭のオブジェクト
        """
        return self.head

    def sorting_append(self, obj, func):
        """
        ソート順に挿入
        :param obj:挿入するオブジェクト
        :param func:比較する関数 func( obj, terget ) : true=手前に挿入 false=挿入しない
        :return:
        """
        ThreadBase.lock()
        if self.tail is None:  # まだ何もLINKされていない
            obj.follow = None
            obj.prev = None
            self.head = obj
            self.tail = obj
            ThreadBase.unlock()
            return

        last = self.tail
        target = self.head
        while target != last:
            if func(obj, target):
                obj.follow = target
                last_prev = target.prev
                target.prev = obj
                if last_prev is None:
                    self.head = obj
                    obj.prev = None
                else:
                    last_prev.follow = obj
                    obj.prev = last_prev
                ThreadBase.unlock()
                return;
            target = target.follow

        obj.follow = None
        last.follow = obj       # 最後に追加
        obj.prev = last
        self.tail = obj
        ThreadBase.unlock()


class LinkedListItem:
    def __init__(self, linked_list):
        self.follow = None
        self.prev = None
        self.linked_list = linked_list

    def append(self):
        self.linked_list.append(self)

    def sorting_append(self, func):
        print("linked_list={0}".format(self.linked_list))
        self.linked_list.sorting_append(self, func)


if __name__ == "__main__":
    class TestItem(LinkedListItem):
        def __init__(self, linked_list, no):
            super().__init__(linked_list)
            self.no = no

        def __str__(self):
            follow = self.follow
            if follow is not None:
                follow = "No.{0}".format(follow.no)
            else:
                follow = "None"

            prev = self.prev
            if prev is not None:
                prev = "No.{0}".format(prev.no)
            else:
                prev = "None"

            text = "No.{0} follow:{1} prev:{2}".format(self.no, follow, prev)
            return text


    def print_list(cont, items):
        print("List:")
        print("TOP:[{0}] TAIL:[{1}]".format(cont.head, cont.tail))
        for i in items:
            print(i)

    def compare( obj1, obj2 ):
        if obj1.no > obj2.no:
            return True
        else:
            return False

    manager = LinkedList()
    obj1 = TestItem(manager, 1)
    obj2 = TestItem(manager, 2)
    obj3 = TestItem(manager, 3)
    obj4 = TestItem(manager, 4)
    obj5 = TestItem(manager, 5)
    item_list = [obj1, obj2, obj3, obj4, obj5]
    print_list(manager, item_list)
    obj1.append()
    print_list(manager, item_list)
    obj2.append()
    print_list(manager, item_list)
    obj3.append()
    obj4.append()
    obj5.append()
    print("-----------------------------")
    print_list(manager, item_list)
    obj = manager.get_top()
    print("Get {0}".format(obj.no))
    print_list(manager, item_list)

    obj = manager.get_top()
    print("Get {0}".format(obj.no))
    print_list(manager, item_list)

    obj = manager.get_top()
    print("Get {0}".format(obj.no))
    print_list(manager, item_list)

    obj = manager.get_top()
    print("Get {0}".format(obj.no))
    print_list(manager, item_list)

    obj = manager.get_top()
    print("Get {0}".format(obj.no))
    print_list(manager, item_list)

    obj = manager.get_top()
    if obj is None:
        print("None")
    else:
        print("Get {0}".format(obj.no))
    print_list(manager, item_list)
    print("-----------------------------")
    manager.sorting_append(  obj2 , compare)
    print_list(manager, item_list)
    manager.sorting_append(  obj1 , compare)
    print_list(manager, item_list)
    manager.sorting_append(  obj3 , compare)
    print_list(manager, item_list)
    manager.sorting_append(  obj5 , compare)
    print_list(manager, item_list)
    manager.sorting_append(  obj4 , compare)
    print_list(manager, item_list)
    print("-----------------------------")
    print_list(manager, item_list)
    obj = manager.get_top()
    print("Get {0}".format(obj.no))
    print_list(manager, item_list)

    obj = manager.get_top()
    print("Get {0}".format(obj.no))
    print_list(manager, item_list)

    obj = manager.get_top()
    print("Get {0}".format(obj.no))
    print_list(manager, item_list)

    obj = manager.get_top()
    print("Get {0}".format(obj.no))
    print_list(manager, item_list)

    obj = manager.get_top()
    print("Get {0}".format(obj.no))
    print_list(manager, item_list)

    obj = manager.get_top()
    if obj is None:
        print("None")
    else:
        print("Get {0}".format(obj.no))
    print_list(manager, item_list)
    print("-----------------------------")
