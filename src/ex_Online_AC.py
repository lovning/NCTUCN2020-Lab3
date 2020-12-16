import sys
import numpy as np

###### Assumption of flow sequence ########
#      Rate = 5 Mbits/sec
#      Duration = 5 sec
###########################################
RATE = 5
DURATION = 5

################## [NOTICE] #############################
#            Don't modify this part                     #
######### Build Lab 3 topology in adjacency matrix ######
def buildTopo(file_name):
  topo_matrix = np.genfromtxt(file_name, delimiter=',')
  return topo_matrix
###################### End here #########################

###################### [TODO] ###########################
#   Modify this part to create online Admission Control algorithm
#   Make decision for each flow one by one
#   Decision:
#       1 -> serve flow, 0 -> reject flow
#   Return decision
#   ex:
#   	return 1
#########################################################  
def Online_AC(flow, prev_flows, topo):
  return 1
  
  # Random decision
  #return np.random.randint(2, size=1)[0]

################### End here ###########################


#################### [NOTICE] ############################
#            Don't modify this part
########### Evaluate Admission Control Decision ##########
#              Evaluation rule
#       Link allocated rate = bandwidth / # of flow remain on this link
#       Flow Allocated Rate = Bottleneck link allocated rate of the flow
#       Allocated Rate > 5 * 80% -> "1"
#       Allocated Rate < 5 * 80% -> "-2"
##########################################################
def Evaluate(flow_sequence, admission_control):
  flow_score = []
  flow_remained = []
  for idx, flow in enumerate(flow_sequence):
  
    flow_score.append([flow[0], flow[1], flow[2], 0])
    
    if admission_control[idx]==1:
      
      ## Previous flow leave
      cur_time = flow[2]
      while flow_remained:
        if  cur_time - flow_remained[0][3]  < DURATION:
          break
        flow_remained.pop(0) 

      flow_remained.append([idx, flow[0], flow[1], flow[2]])
      flow_score[idx][3] = 1

      # Check flows number on each link        
      links = np.zeros((11, 11))
      for f in flow_remained:
        path_id = f[1]-1
        path = paths[path_id]
        for node, next_node in zip(path, path[1:]):
          links[node][next_node] +=1
          links[next_node][node] +=1

      # Store flow  allocated rate < 5 * 80% 
      minus_seq_id = []
      for f in flow_remained:
        path_id = f[1]-1
        path = paths[path_id]
        for node, next_node in zip(path, path[1:]):
          if links[node][next_node] > 2 or links[next_node][node] > 2:
            minus_seq_id.append(f[0])
            break


      ## Update score for flow stay in the network
      for seq_id in minus_seq_id:
        flow_score[seq_id][3] = -2
      #print links

  total_score = 0
  print '\n#########################################################'
  print '###############  Score of each flow  ######################'
  print '#########################################################\n'
  for idx, f in enumerate(flow_score):
    if idx >= 20:
      print ("Flow ({}, {}, {}) score: {}".format(f[0], f[1], f[2], f[3]))
      total_score += f[3]
  print '\n######################################################################'
  print '##########  Result of Online Admission Control Scheduling ############'
  print '######################################################################\n'
  print ("Total score of Online AC is {}".format(total_score))
  ################### End here ###########################  

if __name__=="__main__":

  ################## [NOTICE] ############################
  #            Don't modify this part
  ################## setting  ###########################
  #   flows:
  #     h1->h3, h2->h3, h3->h4, h4->h1, h5->h2
  #
  #   paths:
  #     p1, p2, p3, p4, p5
  #
  #   topo:
  #     "topo_matrix.txt"
  #
  #   Link bandwidth:
  # 	 10 for each link
  ########################################################
  flows = [[1,3], [2, 3], [3, 4], [4, 1], [5, 2]]
  paths = [[1, 6, 7, 8, 3], [2, 7, 8, 3], [3, 8, 9, 4], [4, 9, 10, 6, 1], [5, 10, 6, 7, 2]]

  topo = buildTopo('./topo/topo_matrix.txt') 
  inputfileName = 'testcase.txt'
  ################### End here ###########################

  ################## [NOTICE] ############################
  #            Don't modify this part
  ############### Read Flow sequence #####################
  #   Read flow sequence from "tesetcase.txt"
  #   Store entire flow sequence into 'flow_sequence'
  #   Format:
  #     Src host ID, Dst host ID, arrival time
  #   ex:
  #     flow_sequnence = [[1, 3, 0], [2, 4, 3], [3, 5, 5], ....]
  ########################################################
  flow_sequence = []
  with open(inputfileName) as f:
    for idx, line in enumerate(f):
      tmp = line[:-1].split(' ')
      flow = [int(tmp[0]), int(tmp[1]), float(tmp[2])]
      flow_sequence.append(flow)
  
  ####################  End here #########################
  
  #################### Online AC  ###########################
  admission_control = []
  prev_flows = []
  for idx, flow in enumerate(flow_sequence): 
    if idx < 20:
      decision = 1
      admission_control.append(decision)
      prev_flows.append(flow)
      
    else :
      decision = Online_AC(flow, prev_flows, topo)
      admission_control.append(decision)
      prev_flows.append(flow)
  ###################### End here ###########################

  #################### Evaluate  ###########################
  Evaluate(flow_sequence, admission_control)
  ###################### End here ###########################

  
