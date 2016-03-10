import gdb


class DumpLWLockArray(gdb.Command):


	# List of the LWLockIDs...
	lock_ids = [ 'NullLock',
	'BufFreelistLock',
	'ShmemIndexLock',
	'OidGenLock',
	'XidGenLock',
	'ProcArrayLock',
	'SInvalReadLock',
	'SInvalWriteLock',
	'FreeSpaceLock',
	'WALInsertLock',
	'WALWriteLock',
	'ControlFileLock',
	'CheckpointLock',
	'CheckpointStartLock',
	'CLogControlLock',
	'SubtransControlLock',
	'MultiXactGenLock',
	'MultiXactOffsetControlLock',
	'MultiXactMemberControlLock',
	'RelCacheInitLock',
	'BgWriterCommLock',
	'TwoPhaseStateLock',
	'TablespaceCreateLock',
	'BtreeVacuumLock',
	'AddinShmemInitLock',
	'AutovacuumLock',
	'AutovacuumScheduleLock',
	'SharedSnapshotLock',
	'DistributedLogControlLock',
	'SeqServerControlLock',
	'AOSegFileLock',
	'PersistentObjLock',
	'FileRepShmemLock',
	'FileRepAckShmemLock',
	'FileRepAckHashShmemLock',
	'ChangeTrackingTransitionLock',
	'ChangeTrackingWriteLock',
	'ChangeTrackingCompactLock',
	'MirroredLock',
	'ResQueueLock',
	'FileRepAppendOnlyCommitCountLock',
	'SyncRepLock',
	'ErrorLogLock',
	'FirstWorkfileMgrLock']
	#Not sure what to do with these... will address later
#        FirstWorkfileQuerySpaceLock = FirstWorkfileMgrLock + NUM_WORKFILEMGR_PARTITIONS,
#        FirstBufMappingLock = FirstWorkfileQuerySpaceLock + NUM_WORKFILE_QUERYSPACE_PARTITIONS,
#        FirstLockMgrLock = FirstBufMappingLock + NUM_BUFFER_PARTITIONS,
#        SessionStateLock = FirstLockMgrLock + NUM_LOCK_PARTITIONS,
#
#        /* must be last except for MaxDynamicLWLock: */
#        NumFixedLWLocks,
#
#        MaxDynamicLWLock = 1000000000]
	def __init__(self):
                super (DumpLWLockArray, self).__init__('dump-lwlock-array', gdb.COMMAND_DATA)
		self.fmt_string = 'mutex = %s, releaseOK = %s, exclusive = %s, shared = %s, exclusivePid = %s'

        def invoke(self, args, from_tty):
		lwlock_array = gdb.parse_and_eval('LWLockArray')
		for i in range(0,len(DumpLWLockArray.lock_ids)):
# TODO: I don't know why but I need to subtract 1 here to get the right lock to match the tag
			lwlock = lwlock_array[i + 1]['lock']
			print DumpLWLockArray.lock_ids[i] + ':	' + self.fmt_string%(lwlock['mutex'], lwlock['releaseOK'], lwlock['exclusive'], lwlock['shared'],  lwlock['exclusivePid'])
			# if we are an exclusive or shared lock let's walk the list (head to tail) and print some process info.
			# We can pull the head of the list from the LWLock which points to a PGPROC struct
			# From there we walk the LwWaitLink until null
			pg_proc = lwlock['head']
			while pg_proc:
				print '\t\tPGPROC::\tpid: %s  mppSessionId: %s  lwWaiting: %s  waitLock: %s'%(pg_proc['pid'], pg_proc['mppSessionId'], pg_proc['lwWaiting'], pg_proc['waitLock'])
				pg_proc = pg_proc['lwWaitLink']



DumpLWLockArray()
