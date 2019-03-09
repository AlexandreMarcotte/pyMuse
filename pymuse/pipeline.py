from pymuse.pipelinestages.pipeline_stage import PipelineStage
from pymuse.signal import Signal
from queue import Queue

from pymuse.constants import PIPELINE_QUEUE_SIZE

class PipelineFork():
    def __init__(self, *branches):
        self.forked_branches: list = list(branches)

"""
E.g.: Pipeline(museOSCInputStream.get_signal("eeg"), AStage("1"), PipelineFork([AStage("2"), MuseCSVOutputStream()], [AStage("3")] ))
"""
class Pipeline():

    def __init__(self, input_signal: Signal, *stages):
        self._input_signal = input_signal
        self._stages: list = list(stages)
        self._link_stages(self._stages)
        self._stages[0]._queue_in = self._input_signal.signal_queue

    def _link_pipeline_fork (self, stages: list, index: int):
            for fork in stages[index].forked_branches:
                stages[index - 1].add_queue_out(fork[0].queue_in)
                self._link_stages(fork)

    def _link_stages(self, stages: list):
        for i in range(1, len(stages)):
            if type(stages[i]) == PipelineFork:
                self._link_pipeline_fork(stages, i)
            else:
                stages[i - 1].add_queue_out(stages[i].queue_in)
        if type(stages[-1]) == PipelineStage:
            stages[-1].add_queue_out(Queue(PIPELINE_QUEUE_SIZE))

    def _start(self, stages: list):
        for stage in stages:
            if type(stage) == PipelineFork:
                for forked_branch in stage.forked_branches:
                    self._start(forked_branch)
            else:
                stage.start()

    def start(self):
        self._start(self._stages)
