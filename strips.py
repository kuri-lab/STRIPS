class Module:
    def __init__(self, name, c_list=[], a_list=[], d_list=[], group="action"):
        self.name = name #str型
        self.c_list = c_list #リスト型
        self.a_list = a_list #リスト型
        self.d_list = d_list #リスト型
        self.level = 1 #int型
        self.group = group
        

import copy
import sys
class STRIPS:
    def __init__(self, current_state, goal_state, Search_depth):
        self.goal_state = goal_state
        self.current_state = current_state
        self.Executable = [[]  for i in range(Search_depth+1)]
        self.now_state = [[]  for i in range(Search_depth+2)]
        self.answer_list = []
        self.Search_depth = Search_depth
        self.now_level = 0
        self.pick_up_A = Module("pick_up_A", c_list=["clear_A", "on_table_A","arm_empty"], a_list=["holding_A"], d_list=["on_table_A","arm_empty"], group="action")
        self.pick_up_B = Module("pick_up_B", c_list=["clear_B", "on_table_B","arm_empty"], a_list=["holding_B"], d_list=["on_table_B","arm_empty"], group="action")
        self.pick_up_C = Module("pick_up_C", c_list=["clear_C", "on_table_C","arm_empty"], a_list=["holding_C"], d_list=["on_table_C","arm_empty"], group="action")
        self.stack_A_on_B = Module("stack_A_on_B", c_list=["clear_B", "holding_A"], a_list=["arm_empty", "A_on_B"], d_list=["holding_A","clear_B"], group="action")
        self.stack_A_on_C = Module("stack_A_on_C", c_list=["clear_C", "holding_A"], a_list=["arm_empty", "A_on_C"], d_list=["holding_A","clear_C"], group="action")
        self.stack_B_on_A = Module("stack_B_on_A", c_list=["clear_A", "holding_B"], a_list=["arm_empty", "B_on_A"], d_list=["holding_B","clear_A"], group="action")
        self.stack_B_on_C = Module("stack_B_on_C", c_list=["clear_C", "holding_B"], a_list=["arm_empty", "B_on_C"], d_list=["holding_B","clear_C"], group="action")
        self.stack_C_on_A = Module("stack_C_on_A", c_list=["clear_A", "holding_C"], a_list=["arm_empty", "C_on_A"], d_list=["holding_C","clear_A"], group="action")
        self.stack_C_on_B = Module("stack_C_on_B", c_list=["clear_B", "holding_C"], a_list=["arm_empty", "C_on_B"], d_list=["holding_C","clear_B"], group="action")
        self.unstack_A_on_B = Module("unstack_A_on_B", c_list=["arm_empty", 
                                                               "A_on_B", "clear_A"], a_list=["holding_A","clear_B"], d_list=["arm_empty", "A_on_B"], group="action")
        self.unstack_A_on_C = Module("unstack_A_on_C", c_list=["arm_empty", 
                                                               "A_on_C", "clear_A"], a_list=["holding_A","clear_C"], d_list=["arm_empty", "A_on_C"], group="action")
        self.unstack_B_on_A = Module("unstack_B_on_A", c_list=["arm_empty", 
                                                               "B_on_A", "clear_B"], a_list=["holding_B","clear_A"], d_list=["arm_empty", "B_on_A"], group="action")
        self.unstack_B_on_C = Module("unstack_B_on_C", c_list=["arm_empty", 
                                                               "B_on_C", "clear_B"], a_list=["holding_B","clear_C"], d_list=["arm_empty", "B_on_C"], group="action")
        self.unstack_C_on_A = Module("unstack_C_on_A", c_list=["arm_empty", 
                                                               "C_on_A", "clear_C"], a_list=["holding_C","clear_A"], d_list=["arm_empty", "C_on_A"], group="action")
        self.unstack_C_on_B = Module("unstack_C_on_B", c_list=["arm_empty", 
                                                               "C_on_B", "clear_C"], a_list=["holding_C","clear_B"], d_list=["arm_empty", "C_on_B"], group="action")
        self.put_down_A = Module("put_down_A", c_list=["holding_A"], a_list=["on_table_A","arm_empty"], d_list=["holding_A"], group="action")
        self.put_down_B = Module("put_down_B", c_list=["holding_B"], a_list=["on_table_B","arm_empty"], d_list=["holding_B"], group="action")
        self.put_down_C = Module("put_down_C", c_list=["holding_C"], a_list=["on_table_C","arm_empty"], d_list=["holding_C"], group="action")
        
        self.modules = [self.pick_up_A,self.pick_up_B,self.pick_up_C,
                        self.stack_A_on_B,self.stack_A_on_C,self.stack_B_on_A,self.stack_B_on_C,self.stack_C_on_A,self.stack_C_on_B,
                       self.unstack_A_on_B, self.unstack_A_on_C, self.unstack_B_on_A,self.unstack_B_on_C,self.unstack_C_on_A,self.unstack_C_on_B,
                       self.put_down_A, self.put_down_B,self.put_down_C]
    
    def make_dict(self, c_state):
        module_dict_action = {}
        module_dict_belief = {}
        for module in self.modules:
            c_list_dict = set(module.c_list)
            if c_list_dict.issubset(c_state):
                module_dict_action[str(module.name)] = module.level

        return module_dict_action
    
    def selection(self, c_state):
        action = self.make_dict(c_state)
        keys_of_action = list(action.keys())
        #ここで実行可能リストを配列に
        return keys_of_action
    
    def Loop(self, now_depth):
        my_depth = now_depth
        c_state = copy.deepcopy(self.now_state[my_depth])
        action =  copy.deepcopy(self.selection(c_state))
        if len(action) >= 1:
            self.Executable[my_depth].append(action) 
            
            for i in range(len(self.Executable[my_depth][-1])):
                for module in self.modules:
                    my_depth = now_depth
                    if module.name == action[i]:
                        self.answer_list.append(action[i])
                        c_state = copy.deepcopy(self.now_state[my_depth])
                        for state in module.a_list:
                            c_state.add(state)
                        for state in module.d_list:
                            c_state.discard(state)
                        if self.goal_state.issubset(c_state):
                            print("answer", self.answer_list)
                            sys.exit()
                        else:
                            new_depth = my_depth + 1
                            if new_depth > self.Search_depth:
                                pass
                            else:
                                self.now_state[new_depth] = c_state
                                self.Loop(new_depth)
                        self.answer_list.remove(action[i])
                       
    def global_loop(self):
        self.now_state[0] = self.current_state
        self.Loop(0)
                       
def main():
    current_state = []
    #最初の初期配置
    current_state = set(["clear_A", "on_table_A","clear_B", "on_table_B","clear_C", "on_table_C","arm_empty"])
    #ゴールの位置
    goal_stete = set(["C_on_A","B_on_C", "on_table_A","clear_B","arm_empty"])
    strips = STRIPS(current_state,goal_stete,4)
    strips.global_loop()

main()
