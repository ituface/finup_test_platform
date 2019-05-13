class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    # @param a ListNode
    # @return a ListNode
    def swapPairs(self, head):
        if head != None and head.next != None:
            next = head.next
            head.next = self.swapPairs(next.next)
            next.next = head
            return next
        return head


#1->2->3->4


l1=ListNode(1)
l2=ListNode(2)
l3=ListNode(3)
l4=ListNode(4)
l1.next=l2
l2.next=l3
l3.next=l4


s=Solution()
a=s.swapPairs(l1)
while a:
    print(a.val)
    a=a.next
