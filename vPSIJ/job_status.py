from enum import Enum, auto

class status( Enum ):
  new = auto()
  submitting = auto()
  queuing = auto()
  running = auto()
  cleanup = auto()
  completed = auto()
  failed = auto()
  canceled = auto()
