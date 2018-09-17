import re
import sys
from copy import copy

#superclass for all instructions
class TACInstr(object):

    live_in = set()
    live_out= set()

    def __init__(self):
        self.block = None
        self.index = -1
        self.isInvariant = False



class TACDefault(TACInstr):
    def __init__(self, assignee, typ):
        self.assignee = assignee
        self.typ = typ
    
    def __str__(self):
        return str(self.assignee) + ' <- default ' + str(self.typ)
    
class TACPlus(TACInstr):
    def __init__(self, assignee, op1, op2):
        self.assignee = assignee
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        return str(self.assignee) + ' <- + ' + str(self.op1) + ' ' + str(self.op2)

class TACMinus(TACInstr):
    def __init__(self, assignee, op1, op2):
        self.assignee = assignee
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        return str(self.assignee) + ' <- - ' + str(self.op1) + ' ' + str(self.op2)

class TACTimes(TACInstr):
    def __init__(self, assignee, op1, op2):
        self.assignee = assignee
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        return str(self.assignee) + ' <- * ' + str(self.op1) + ' ' + str(self.op2)

class TACDivide(TACInstr):
    def __init__(self, assignee, op1, op2):
        self.assignee = assignee
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        return str(self.assignee) + ' <- / ' + str(self.op1) + ' ' + str(self.op2)

class TACAssign(TACInstr):
    def __init__(self, assignee, op1):
        self.assignee = assignee
        self.op1 = op1

    def __str__(self):
        return str(self.assignee) + ' <- ' + str(self.op1)

class TACNew(TACInstr):
    def __init__(self, assignee, typ):
        self.assignee = assignee
        self.op1 = op1

    def __str__(self):
        return str(self.assignee) + ' <- new ' + str(self.typ)

class TACCall(TACInstr):
    def __init__(self, assignee, function, args):
        self.assignee = assignee
        self.function = function
        self.args = args

    def __str__(self):
        args = ' '.join(str(arg) for arg in self.args)
        return str(self.assignee) + ' <- call ' + str(self.function) + ' ' + args

class TACLabel(TACInstr):
    def __init__(self, label):
        self.label = label

    def __str__(self):
        return 'label ' + str(self.label)


class TACNot(TACInstr):
    def __init__(self, assignee, op1):
        self.assignee = assignee
        self.op1 = op1

    def __str__(self):
        return str(self.assignee) + ' <- not ' + str(self.op1)

class TACBt(TACInstr):
    def __init__(self, op1, label):
        self.op1 = op1
        self.label = label

    def __str__(self):
        return 'bt ' + str(self.op1) + ' ' + str(self.label)

class TACJmp(TACInstr):
    def __init__(self, label):
        self.label = label

    def __str__(self):
        return 'jmp ' + str(self.label)

class TACLt(TACInstr):
    def __init__(self, assignee, op1, op2):
        self.assignee = assignee
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        return str(self.assignee) + ' <- < ' + str(self.op1) + ' ' + str(self.op2)

class TACLe(TACInstr):
    def __init__(self, assignee, op1, op2):
        self.assignee = assignee
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        return str(self.assignee) + ' <- <= ' + str(self.op1) + ' ' + str(self.op2)

class TACEq(TACInstr):
    def __init__(self, assignee, op1, op2):
        self.assignee = assignee
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        return str(self.assignee) + ' <- = ' + str(self.op1) + ' ' + str(self.op2)

class TACNegate(TACInstr):
    def __init__(self, assignee, op1):
        self.assignee = assignee
        self.op1 = op1

    def __str__(self):
        return str(self.assignee) + ' <- ~ ' + str(self.op1)

class TACIsvoid(TACInstr):
    def __init__(self, assignee, op1):
        self.assignee = assignee
        self.op1 = op1

    def __str__(self):
        return str(self.assignee) + ' <- isvoid ' + str(self.op1)

class TACInt(TACInstr):
    def __init__(self, assignee, intval):
        self.assignee = assignee
        self.intval = intval

    def __str__(self):
        return str(self.assignee) + ' <- int ' + str(self.intval)

class TACString(TACInstr):
    def __init__(self, assignee, string):
        self.assignee = assignee
        self.string = string

    def __str__(self):
        return str(self.assignee) + ' <- string\n' + str(string)

class TACBool(TACInstr):
    def __init__(self, assignee, boolean):
        self.assignee = assignee
        self.boolean = boolean

    def __str__(self):
        return str(self.assignee) + ' <- bool ' + str(self.boolean)

class TACReturn(TACInstr):
    def __init__(self, op1):
        self.op1 = op1

    def __str__(self):
        return 'return ' + str(self.op1)




class TACBasicBlock(object):
    def __init__(self, instructions):
    
        self.instructions = instructions

        self.label = self.instructions[0].label
    
        self.child_labels = [ins.label for ins in self.instructions
                            if isinstance(ins, TACBt) or isinstance(ins, TACJmp)]

        for idx, ins in enumerate(self.instructions):
            ins.block = self
            ins.index = idx

        self.children = []
        self.parents = []

        self.incoming = None
        self.outgoing = None
        self.reached = False

        # list of sets, each instruction corresponds to an entry in this list
        # each element of this list is the set of live variables present after executing that instruction
        self.livelist = []

        # list of sets, each instruction corresponds to an entry in this list
        # each element of this list is the 
        self.reachlist = []
    
        #dominator set
        self.dom = set()

        # dominance frontier
        self.df = set()

        #immediate dominator
        self.idom = None

        #dominator tree
        self.domtree = set()

        #back pointers in dom tree
        self.domback = set()

        # set of live in and out variables for each block
        self.live_in = set()
        self.live_out = set()


        # helper variable
        self.changed = False


        # set of definitions for reachability
        self.reach_in = set()
        self.reach_out = set()

    def gen_live_in(self):
        #iterate in reverse order
        self.changed = False
        self.livelist = []
        mylive = copy(self.live_out)

        self.instructions[-1].live_out = copy(self.live_out)

        for i, ins in enumerate(reversed(list(self.instructions))):
            #the first instruction is different... for all the others,
            # copy the live in set from the subsequent instruction as
            # the live out of this instruction
            if i > 0:
                ins.live_out = copy(self.instructions[len(self.instructions)-i].live_in)
                ins.live_in = copy(ins.live_out)


            # make liveness decisions for variables based on the type of
            # each instruction
            if isinstance(ins, TACCall):
                ins.live_in.discard(ins.assignee)
                mylive.discard(ins.assignee)
                for arg in ins.args:
                    ins.live_in.add(arg)
                    mylive.add(arg)
            else:
                if hasattr(ins, 'assignee'):
                    ins.live_in.discard(ins.assignee)
                    mylive.discard(ins.assignee)
                    if hasattr(ins, 'op1'):
                        ins.live_in.add(ins.op1)
                        mylive.add(ins.op1)
                    if hasattr(ins, 'op2'):
                        ins.live_in.add(ins.op2)
                        mylive.add(ins.op2)
                elif isinstance(ins, TACReturn):
                    ins.live_in.add(ins.op1)
                    mylive.add(ins.op1)
                elif isinstance(ins, TACBt):
                    ins.live_in.add(ins.op1)
                    mylive.add(ins.op1)

            self.livelist.insert(0, set(mylive))

        if self.live_in ^ mylive: 
            self.changed = True
        # propogate change to parents
        for parent in self.parents:
            parent.live_out.update(mylive)
        self.live_in = mylive
        
    def gen_reach_out(self):
        self.changed = False
        self.reachlist = []
        myreach = copy(self.reach_in)
        for ins in list(self.instructions):
            if hasattr(ins, 'assignee'):
                for reach_in_inst in self.reach_in:
                    if reach_in_inst.assignee == ins.assignee:
                        myreach.discard(reach_in_inst)

                for reach_in_inst in list(self.instructions):
                    if hasattr(reach_in_inst, 'assignee') and reach_in_inst.assignee == ins.assignee:
                        myreach.discard(reach_in_inst)
                myreach.add(ins)
            self.reachlist.append(set(myreach))

        if self.reach_out ^ myreach:
            self.changed = True
        for child in self.children:
            child.reach_in.update(myreach)
        self.reach_out = myreach


    def clear_reach(self):
        self.reach_in = set()
        self.reach_out = set()
        self.reachlist = []

    def clear_liveness(self):
        self.live_in = set()
        self.live_out = set()
        for ins in self.instructions:
            self.live_in.clear()
            self.live_out.clear()
        self.livelist = []

    def remove_dead(self):
        self.changed = False
        revised_instructions = []
#        revised_liveness = []
        

#        mylivelist = list(self.livelist)
#        mylivelist.append(self.live_out)
#        mylivelist.pop(0)
#
        for inst in list(reversed(self.instructions)):
            if (not isinstance(inst, TACCall)) and hasattr(inst, 'assignee') and inst.assignee not in inst.live_out:
                print 'Removing ' + str(inst)
                self.changed=True
            else:
                revised_instructions.append(inst)


        self.instructions = list(reversed(revised_instructions))

##        print 'Dead removal ' + self.label
#
#        for (inst, liveness) in zip(reversed(self.instructions), reversed(mylivelist)):
##            print str(inst) + ' ' + str(liveness)
#            if (not isinstance(inst, TACCall)) and hasattr(inst, 'assignee') and inst.assignee not in liveness:
##                print 'Removing ' + str(inst) + ' because ' + str(inst.assignee) + ' not in ' + str(liveness)
##                print str(mylivelist)
#                self.changed = True
#            else:
#                revised_instructions.append(inst)
#                revised_liveness.append(liveness)

#        self.liveness = list(reversed(revised_liveness))
#        self.instructions = list(reversed(revised_instructions))

    
    def strictlyDominates(self, other):
        if (not self.label == other.label) and self in other.dom:
            return True
        else:
            return False

    def __str__(self):

        
        s = 'Label : ' + str(self.label) + '\n'
        s += 'Parents : ' + str([parent.label for parent in self.parents]) + '\n'
        for idx, inst in enumerate(self.instructions):
            s += str(idx) + '. ' + str(inst) + '\t[' + ", ".join(map(str,inst.live_in)) + '] \t[' + ", ".join(map(str, inst.live_out)) + '] \n'
#        for idx, (item, live) in enumerate(zip(self.instructions, self.livelist)):
#            s += str(idx) + '. ' + str(item) + '\t[' + ", ".join(map(str,live)) + '] \n'
            #s += '\t' + print_reach(self.reachlist[idx]) + '\n'
        s += 'Children : ' + str([child.label for child in self.children]) + '\n'
        s += 'LIVE_in : ' + ", ".join(map(str,self.live_in)) + '\n'
        s += 'LIVE_out : ' + ", ".join(map(str,self.live_out)) + '\n'
#        s += 'REACH_in : ' + print_reach(self.reach_in) + '\n'
#        s += 'REACH_out : ' + print_reach(self.reach_out) + '\n'
#        s += 'DOM : ' + ", ".join(map(TACBasicBlock.getLabel,self.dom)) + '\n'
#        s += 'IDOM : ' + str(self.idom) + '\n'
        return s

    def getLabel(self):
        return self.label

def print_reach(mylist):
    string = ""
    for myinst in mylist:
        if not re.search('t\$', myinst.assignee):
            string += str(myinst) + ", "

    return string

def find_end_blocks(blocks):
    endblocks = []
    for block in blocks:
        if len(block.children) == 0:
            endblocks.append(block)

    return endblocks
 


def do_liveness_fixpoint(blocks):
    for b in blocks:
        b.changed = False
    fixedPointReached = False
    # keep doing it until everything stabilizes
    while not fixedPointReached:
        #assume it's done unless we're told otherwise (if any block's live sets are changed)
        fixedPointReached = True
        for block in blocks:
            mylive = set()
            # a block's live_out set is the union of all its children's live_in sets
            for child in block.children:
                mylive.update(child.live_in)
            block.live_out = set(mylive)
            
            # each block, we go through instructions in reverse a track live sets
            block.gen_live_in()

            # if there are no more changes, then fixed point is reached and we end
            if block.changed:
                fixedPointReached = False

class NaturalLoop(object):
    def __init__(self, header, backedge, body):
        self.header = header
        self.backedge = backedge
        self.body = body
    
    def __str__(self):
        return "Natural Loop: H " + str(self.header.label) + " B " + str(self.backedge.label) + " Body " + ", ".join(map(TACBasicBlock.getLabel, self.body)) + '\n'


def do_loop_detection(blocks):
    loops = []
    for h in blocks:
        for n in blocks:
            if (not h in n.dom) or (h == n) or (not h in n.children):
                continue
            reached_blocks = set()
            worklist = []
            worklist.append(n)
            while (len(worklist) > 0):
                v = worklist.pop()
                if (not v in reached_blocks):
                    reached_blocks.add(v)
                    for c in v.parents:
                        if (not c == h):
                            worklist.append(c)
            reached_blocks.add(h)

            if len(reached_blocks) > 0:
                loops.append(NaturalLoop(h,n,reached_blocks))
    
    return loops
#    for l in loops:
#        print str(l)
    
def do_loop_invariants(loops):
    invariants = []
    for l in loops:
        for b in l.body:
            if b == l.header:
                continue
            for i in b.instructions:
                if not hasattr(i, 'assignee'):
                    continue
                isInvariant = True
                op1 = ""
                op2 = ""
                
                if (hasattr(i, 'op1')):
                    op1 = i.op1
                if (hasattr(i, 'op2')):
                    op2 = i.op2



                for reach_inst in b.reach_in:
                    if str(op1) == reach_inst.assignee or str(op2) == reach_inst.assignee:
                        if (reach_inst.block in l.body):
                            isInvariant=False
                if isInvariant:
                    print "Instruction " + str(i) + " is loop invariant."
                    i.isInvariant = True
                    if isHoistable(i, l):
                        print "Hoistable"
                    else:
                        print "Not hoistable"

def isHoistable(ins, loop):
    exits = set()
    d = ins.block
    t = ins.assignee
    for b in loop.body:
        for c in b.children:
            if not c in loop.body:
                exits.add(b)
                print "Block " + str(b.label) + " exits"
        for i in b.instructions:
            if i == ins:
                continue
             
            if hasattr(i, 'assignee') and str(t) == str(i.assignee):
                return False

            if (hasattr(i, 'op1') and i.op1 == t) or (hasattr(i, 'op2') and i.op2 == t):
                for j in i.block.reachlist[i.index]:
                    if j.assignee == t and not j == ins:
                        return False

    for e in exits:
        if t in e.live_out and d not in e.dom:
            return False
    
    return True




    


def do_reachability_fixpoint(blocks):
    for b in blocks:
        b.changed = False
    fixedPointReached = False
    while not fixedPointReached:
        fixedPointReached = True
        for block in blocks:
            my_reach = set()
            # a block's reach_in set is the union of all its parent's reach_out sets
            for parent in block.parents:
                my_reach.update(parent.reach_out)
            block.reach_in = set(my_reach)

            block.gen_reach_out()

            if block.changed:
                fixedPointReached = False

def do_dominance_fixpoint(blocks):
    #find strt block
    start = None
    for b in blocks:
        if b.parents == []:
            start = b
            break

    start.dom.add(start)
    for b in blocks:
        if b == start:
            continue
        for q in blocks:
            b.dom.add(q)

    fixedPointReached = False
    while not fixedPointReached:
        fixedPointReached = True
        for b in blocks:
            if b == start:
                continue
            my_dom_p = set()
            my_dom_p.update(copy(b.parents[0].dom))
            for parent in b.parents:
                my_dom_p &= copy(parent.dom)

            my_dom_p.add(b)
            if not my_dom_p == b.dom:
                fixedPointReached = False

            b.dom = my_dom_p

def idoms(blocks):
    for b in blocks:
        # starting block (i.e., the one with no parents) has no idom
        if b.parents == []:
            continue
        idom = None
        # let's check if node 'dom' is the idom of b
        for dom in b.dom:
            #check each node that strictle dominates b...
            if not dom.strictlyDominates(b):
                continue
            # now we know dom strictly dominates b...
            # for each block X that strictly dominates b
            #   we need to make sure that dom does not strictly dominate X
            for testblock in b.dom:
                if not testblock.strictlyDominates(b):
                    continue
                if testblock == dom:
                    continue
                if dom.strictlyDominates(testblock):
                    break
            else:
                idom = dom

        b.idom = idom.label
        # also construct the dominator tree while we're here.
        idom.domtree.add(b)
        b.domback.add(idom)




def remove_dead (blocks):
    do_liveness_fixpoint(blocks)
    for block in blocks:
        block.remove_dead()
#    fixedPointReached = False
#    while not fixedPointReached:
#        fixedPointReached = True
#        for block in blocks:
#            block.clear_liveness()
#        
#        do_liveness_fixpoint(blocks)
#
#        for block in blocks:
#            block.remove_dead()
#
#        for block in blocks:
#            if block.changed:
#                fixedPointReached = False


def tac_from_file(filename):
    f = open(filename)
    tac = []
    for line in f:
        tac.append(line.rstrip('\n').rstrip('\r'))
    f.close()
    return tac

def make_inst_list(tac):
    inst_list = []
    for tacinst in tac:
        if tacinst == "":
            continue
        myinst = tacinst.split(' ')
        if myinst[0] == "label":
            thelabel = myinst[1]
            inst_list.append(TACLabel(thelabel))
        elif myinst[0] == "bt":
            inst_list.append(TACBt(myinst[1], myinst[2]))
        elif myinst[0] == "comment":
            pass
        elif myinst[0] == "jmp":
            inst_list.append(TACJmp(myinst[1]))
        elif myinst[0] == "return":
            inst_list.append(TACReturn(myinst[1]))
        else:
            # remember myinst[1] should always be '<-' now...
            #arithmetic
            if myinst[2] == '+':
                inst_list.append(TACPlus(myinst[0], myinst[3], myinst[4]))
            elif myinst[2] == '-':
                inst_list.append(TACMinus(myinst[0], myinst[3], myinst[4]))
            elif myinst[2] == '*':
                inst_list.append(TACTimes(myinst[0], myinst[3], myinst[4]))
            elif myinst[2] == '/':
                inst_list.append(TACDivide(myinst[0], myinst[3], myinst[4]))
            #comparisons
            elif myinst[2] == '<':
                inst_list.append(TACLt(myinst[0], myinst[3], myinst[4]))
            elif myinst[2] == '<=':
                inst_list.append(TACLe(myinst[0], myinst[3], myinst[4]))
            elif myinst[2] == '=':
                inst_list.append(TACEq(myinst[0], myinst[3], myinst[4]))
            #constants
            elif myinst[2] == 'int':
                inst_list.append(TACInt(myinst[0], myinst[3]))
            elif myinst[2] == 'boolean':
                inst_list.append(TACBool(myinst[0], myinst[3]))
            elif myinst[2] == 'string':
                thestring = tac.next() 
                inst_list.append(TACString(myinst[0], thestring))
            #other
            elif myinst[2] == 'not':
                inst_list.append(TACNot(myinst[0], myinst[3]))
            elif myinst[2] == '~':
                inst_list.append(TACNegate(myinst[0], myinst[3]))
            elif myinst[2] == 'new':
                inst_list.append(TACNew(myinst[0], myinst[3]))
            #default init...
            elif myinst[2] == 'default':
                inst_list.append(TACDefault(myinst[0], myinst[3]))
            #isvoid
            elif myinst[2] == 'isvoid':
                inst_list.append(TACIsvoid(myinst[0], myinst[3]))
            #call function (no args at the moment)
            elif myinst[2] == 'call':
                inst_list.append(TACCall(myinst[0], myinst[3], myinst[4:]))
            elif len(myinst) == 3 and myinst[1] == '<-':
                inst_list.append(TACAssign(myinst[0], myinst[2]))
    return inst_list

                


def make_bbs(inst_list):
    myblocks = []
    blocked_instructions = []

    #  blocked_instructions 
    #   [ [label, assign, addition, jmp ], [label, subtraction, lt, bt
    #   ], [label, assign, return ] ]
    #

    for instruction in inst_list:
        if isinstance(instruction, TACLabel):
            blocked_instructions += [[]]
        blocked_instructions[-1] += [instruction]

    block_dict = {}

    for block in blocked_instructions:
        newblock = TACBasicBlock(block)
        myblocks += [newblock]
        block_dict[newblock.label] = newblock


    for block in myblocks:
        for child_label in block.child_labels:
            block.children += [block_dict[child_label]]
        del block.child_labels

    for block in myblocks:
        for child in block.children:
            child.parents += [block]

    return myblocks



def main():

    filename = sys.argv[1]
    tac = tac_from_file(filename)
    insts = make_inst_list(tac)
    
    myblocks = make_bbs(insts)


    # Conduct liveness analysis (for dead-code elimination later)
    do_liveness_fixpoint(myblocks)

    
    
    # For Loop-invariant code motion:
    # 1) We need to know the definitions that REACH expressions later in
    #    the loop.
    #     
    #     x = 5
    #     i = 0
    #     while ( a < b )
    #       a = a + b + i          # The definitions (1) i = 0  AND  (2) i = i + x  reach this line
    #       c = x                  # However, the only definition of x (x=5) is OUTSIDE the loop, so this assignment is loop invariant
    #       d = c + x              # (c=x) and (x=5) both reach this definition.  Because c=x is loop invariant, this assignment is as well
    #

    # We do a reachability analysis to find out which definitions reach each expression in the program:
    #do_reachability_fixpoint(myblocks)

    # 2) Once we know the reachability information in our program, we need to find loops next.
    # 
    # We use the notion of DOMINANCE to find where loops occur in the control flow graph.  
    #
   
   
    # We say that node A dominates a node X if every path through the graph that
    # passes through X also passes through A.  With regard to loops, we use
    # dominance to establish a guarantee: Regardless of what a loop body
    # contains, you know that the loop head (i.e., the conditional check) must
    # be on every path through the loop.  So, if we can find a group of nodes
    # that are all dominated by a single node, we might conclude that node is a
    # loop head
 
    # We do an analysis to establish the sets of nodes that dominate each node in the control flow graph
    #do_dominance_fixpoint(myblocks)


     

    # Some analyses benefit from knowing a specific IMMEDIATE DOMINATOR.
    #  Dominance alone isn't enough to determine loops.  Loops also require the existence of particular edges in the control flow graph.
    #  Basically, a loop needs to have an incoming edge from the bottom of the loop (representing the jump back to the loop header to reevaluate the condition)
    #  We identify the bottom of the loop by establishing the collection of nodes that share an immediate dominator and that have an edge going to that immediate dominator.
    # The immediate dominator of node N is the node that dominates N but does not dominate any other node that dominates N
    #
    #  Consider the graph:
    # 
    #                  A <------
    #                  |       |
    #             B<---|--->C  |
    #             |         |  |
    #          D<-|->E v----|  |
    #          |     |-v       |
    #          |------>F--------
    #
    #    Even though B dominates both D and E, we say that A immediately dominates D and E because it is the only node that is not itself dominated by other dominators of D and E
    #
    #idoms(myblocks)
    


    # Next, we can actually perform the loop detection using dominance information.
    #  We 1) find a backedge:  an edge from A -> B such that B dominates A
    #     2) compute Natural Loop of backedge:  B is the loop header, body is the set of all nodes that reach A without going through B
    
    #loops = do_loop_detection(myblocks)

    # Note that nested loops can be a bit more complicated (e.g., multiple
    # loops can share the same header).  This does not occur in Cool,
    # particularly if you are generating ASM in a principled manner.  Nested
    # loops naturally fall out of this computation.



    # Finally, we can look at each loop and find the code inside that is loop invariant.
    # An expression a <- OP b c is loop-invariant if each operand is 1) Constant, 2) defined only outside the loop, or 3) has exactly one loop-invariant computation

    #do_loop_invariants(loops)
   


    # We save DCE for the end...
    remove_dead(myblocks)

    for block in myblocks:
        print "%s\n" % str(block)
        #for instruction in block.instructions:
        #    print str(instruction)
    
if __name__ == '__main__':
    main()