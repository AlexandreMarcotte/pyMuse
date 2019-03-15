from dataclasses import dataclass
from datetime import datetime

from pymuse.utils.stoppablequeue import StoppableQueue

@dataclass
class SignalData():
    time: float
    values: list


class Signal():

    def __init__(self, length: int, acquisition_frequency: float):
        self._signal_queue: StoppableQueue = StoppableQueue(length)
        self._signal_period: float = (1 / acquisition_frequency)
        self._data_counter: int = 0

    @property
    def signal_queue(self) -> StoppableQueue:
        return self._signal_queue

    def push(self, data_list: list):
        time = self._data_counter * self._signal_period
        signal_data: SignalData = SignalData(time, data_list)
        self._signal_queue.put(signal_data, True, self._signal_period)
        self._data_counter += 1

    def pop(self) -> SignalData:
        return self._signal_queue.get(True)
