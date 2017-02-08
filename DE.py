def test_QC20817_ChunkinatorOnActiveCluster():
    """
    Test purpose:
    mark Xenv10 as failed using chuck
    detect Xenv10 state with chunkinator, dump
    revert back to healthy using chuck
    detect healthy satate with chunkinator
    IMPORTANT ! REQUIRED TO BE EXECUTED ON ACTIVECLUSTER !
    :return:None
    """
    from testfunctions.chuck_norris import createChunkinatorOutPutDictionary, XenvsStatusFailed
    # region test Variables
    #  Variables required for TC ############################
    nodeDict = {}  # Node name (key) ,  (xenv output)value )
    nodeKeysList = []  # Node names list
    xenvValues = []  # xenv output
    curNodeKey = None  # node name e.g Node 8 , Node 9
    isThisLineXenvValue = False  # internal for parsing  chunkiknator output
    areOtherXenvsHealthy = False  # result of XenvsStatusFailed - based on this we decide if result is as expected
    isKeyfound = False  # internal for iterating over Xenvs
    node_state_command = "cluster.sym_repo.SymPersObjMdl[0].state"
    invalid_xenv10_state = "16"
    valid_xenv10_state = "4"
    #  Variables required for TC ############################
    # endregion

    chuck_norris.reportObj.Info('Starting test QC-20817\n\n', color='bright blue')
    chuck_norris.TSF_DeployChuckNorris('<cluster>.xms',
                                       '<options>.CNVersion',
                                       cnInstallocation='/var/tmp/',
                                       latestVersion=False)
    chuck_norris.TSF_ConnectToChuckNorris('<cluster>.xms',
                                          '<options>.CNVersion',
                                          '<options>.CNRelease',
                                          stopSys='n',
                                          stopPMs='n')
    # cluster is NOT stopped as required by TC
    # changing Xenv 10 status to FAILED and in transition
    chuck_norris.reportObj.Info('Changing Node 8 Xenv 10 node 8 state to FAILED ....\n', color='bright blue')
    chuck_norris.TSF_GetValFromChuckNorris('\n')
    chuck_norris.TSF_GetValFromChuckNorris(node_state_command + " = " + invalid_xenv10_state)
    chuck_norris.TSF_GetValFromChuckNorris('\n')
    message = "Changed Node 8 Xenv 10 state to FAILED, dumping...symrepo... "
    chuck_norris.reportObj.Info(message, color='bright blue')
    chuck_norris.TSF_GetValFromChuckNorris('dump symrepo')
    chuck_norris.TSF_GetValFromChuckNorris('cluster.parallel_jr_dump()')
    chuck_norris.TSF_GetValFromChuckNorris('\n')
    chuck_norris.TSF_GetValFromChuckNorris('exit()')
    # reconnecting to CN - here we have a framework performance issue
    chuck_norris.TSF_ConnectToChuckNorris('<cluster>.xms',
                                          '<options>.CNVersion',
                                          '<options>.CNRelease',
                                          stopSys='n',
                                          stopPMs='n')
    chuck_norris.reportObj.Info('validating with Chunkinator changed value \n', color='bright blue')
    chuck_norris.TSF_GetValFromChuckNorris("execfile('/var/tmp/chucknorris/scripts/chunkinator/import_and_run.py')"
                                           , "chunkinatorOutPut")
    chunkinatorOutput = testInit.GetVar("chunkinatorOutPut")
    # test logic
    createChunkinatorOutPutDictionary(chunkinatorOutput, nodeDict, isThisLineXenvValue,
                                      xenvValues, nodeKeysList, curNodeKey) # parsing output
    assert XenvsStatusFailed(nodeDict, areOtherXenvsHealthy, isKeyfound), \
        "Expecting FAILED status on Xenv 10 , Aborting test ! " # validating Xenv 10 status
    chuck_norris.reportObj.Info('Changing node state to back to HEALTHY ....\n', color='bright blue')
    chuck_norris.TSF_GetValFromChuckNorris('\n')
    # reverting Xenv 10 state to "healthy"
    chuck_norris.TSF_GetValFromChuckNorris(node_state_command + " = " + valid_xenv10_state)
    chuck_norris.TSF_GetValFromChuckNorris('\n')
    message = "Changed Xenv10 node 8 state back to Healthy"
    chuck_norris.reportObj.Info(message, color='bright blue')
    chuck_norris.TSF_GetValFromChuckNorris('dump symrepo')
    chuck_norris.TSF_GetValFromChuckNorris('cluster.parallel_jr_dump()')
    chuck_norris.TSF_GetValFromChuckNorris('exit()')
    # TODO Connecting to CN for the third time - here we have a HUGE performance drop,
    # TODO add this to framework discussion when the time is right
    chuck_norris.TSF_ConnectToChuckNorris('<cluster>.xms',
                                          '<options>.CNVersion',
                                          '<options>.CNRelease',
                                          stopSys='n',
                                          stopPMs='n')

    chuck_norris.reportObj.Info('validating with Chunkinator changed value  - EXPECTING healthy!\n',
                                color='bright blue')
    chuck_norris.TSF_GetValFromChuckNorris("\n")
    chuck_norris.TSF_GetValFromChuckNorris("execfile('/var/tmp/chucknorris/scripts/chunkinator/import_and_run.py')"
                                           , "chunkinatorOutPut")
    chunkinatorOutput = testInit.GetVar("chunkinatorOutPut")
    createChunkinatorOutPutDictionary(chunkinatorOutput, nodeDict, isThisLineXenvValue,
                                      xenvValues, nodeKeysList, curNodeKey) # parsing new output
    assert not XenvsStatusFailed(nodeDict, areOtherXenvsHealthy, isKeyfound),\
        "Expecting 'healthy' status on all XENV , Aborting test ! " # validating Xenv10 healthy
    chuck_norris.reportObj.Info('Xenv10 is healthy failure reverted, finishing test!\n'
                                , color='bright blue')
    chuck_norris.TSF_GetValFromChuckNorris('exit()')
    chuck_norris.reportObj.Info('Finished test_QC20817_ChunkinatorOnActiveCluster', color='green')


	
	@TSFDecorator
def createChunkinatorOutPutDictionary(chunkinatorOutput, nodeDict, isThisLineXenvValue,
                                      xenvValues, nodeKeysList, curNodeKey):
    """
    :param chunkinatorOutput:  list returned from chuck_norris.
    :type chunkinatorOutput: list
    :param nodeDict : properly parsed chunkinator output ,Node name (key),(xenv output)value )
    :type nodeDict: dictionary
    :param isThisLineXenvValue: internal variable  for parsing  chunkiknator output , used
    to determine if 'Xenv' is present in line
    :type isThisLineXenvValue: boolean
    :param xenvValues: list containing Xenv values
    :type xenvValues: list
    :param nodeKeysList:  list of node names - used in nodeDict as key
    :type nodeKeysList: list
    :param curNodeKey: variable for iterating over nodes
    :type curNodeKey: list
    :return: None
    """

    for line in chunkinatorOutput:
        if isThisLineXenvValue and curNodeKey:
            matchXenv = re.search(r'Xenv [0-9]+', line)  # get Xenv number
            if matchXenv:
                xenvName = matchXenv.group()
                xenvValues.append(xenvName)
                nodeDict[curNodeKey].append(line)
                continue
        match = re.search(r'Node [0-9]+', line)
        if match:  # Node found
            isThisLineXenvValue = True
            curNodeKey = match.group()  # Getting Node name as key
            nodeKeysList.append(curNodeKey)  # Appending key to list for usage in nodeDict
            nodeDict[curNodeKey] = []
            continue

#=======================================================================================================

@xioDecorators.TCSetup('QC-35786')
def test_QC35786_StartCNADuringRollingRebootOfSymNode():
    """
        Log in to SYM node and kill "sym" process every 10 seconds
        start CN during that state
        To recover run:cluster.start_all_pms() and then cluster.start_cluster_naturally()
    """
    chuck_norris.reportObj.Info("\n\nStarting test QC-35786 - start CN during rolling SYM reboot \n", color='blue')
    chuck_norris.TSF_DeployChuckNorris("<cluster>.xms", "<options>.CNVersion", cnInstallocation="/var/tmp/",
                                       latestVersion=True)

    chuck_norris.reportObj.Info("\n running process of kiling sym cluster state will be unknown \n", color='blue')
    cluster.TSF_MurderSymRepeatedly("<cluster>")
    chuck_norris.reportObj.Info("\n\n Starting CN with --stop-cluster-violently flag \n", color='blue')
    chuck_norris.TSF_ConnectToChuckNorris("<cluster>.xms", "<options>.CNVersion", "<options>.CNRelease", stopSys="Skip",
                                          stopPMs="Skip", cn_start_flags=["--stop_cluster_violently"])

    chuck_norris.TSF_GetValFromChuckNorris("cluster.start_all_pms()")
    chuck_norris.TSF_GetValFromChuckNorris("cluster.start_cluster_naturally()")
    chuck_norris.TSF_GetValFromChuckNorris("exit()")

    # clear the process of sym_killer
    testInit.ts_vars.GetTSVar("RollingSymProcess").terminate()
    testInit.ts_vars.GetTSVar("SymNodeToClean").Run("rm -rf sym_killer.sh")

    cluster.TSF_WaitForClusterState("<cluster>", expectedState="active")
    chuck_norris.reportObj.Info("Finished test QC-35786 - start CN during rolling SYM reboot", color='blue')


	
	
@TSFDecorator
def TSF_MurderSymRepeatedly(cluster):
    """this function repeatedly kills SYM process on SYM node for required amount of time
        creates a bash script on node , applies permissions and executes it
        sets to ts_vars two objects process to kill and node to remove files from

    :param clusterObj: cluster to test
    :type  clusterObj: xtremio.cluster.Cluster
    :return:None
    """
    symNode = cluster.GetSymNode()
    symNode.Run('printf "s=1\n e=60\n for ((;s<e;s++))\n do\n sleep 7\n '
                'pgrep -f xenv_1.ini | xargs kill -9 \n done\n" > sym_killer.sh', blocking=True)
    symNode.Run('chmod +x sym_killer.sh', blocking=True)
    p = symNode.Run("./sym_killer.sh", blocking=False, stdout=True)

    # providing process and file name to delete
    ts_vars.SetTSVar("RollingSymProcess", p)
    ts_vars.SetTSVar("SymNodeToClean", symNode)

	
	
	
