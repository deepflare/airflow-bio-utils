from typing import Callable, Sequence, Union

from airflow.operators.python_operator import PythonOperator
from airflow.utils.decorators import apply_defaults

from airflow_bio_utils.sequences.merge import merge_sequences

from .utils import resolve_callable


class SequenceMergeOperator(PythonOperator):
    paths: Union[Sequence[str], Callable[..., Sequence[str]]]
    output_path: Union[str, Callable[..., str]]

    @apply_defaults
    def __init__(
        self,
        paths: Union[Sequence[str], Callable[..., Sequence[str]]],
        output_path: Union[str, Callable[..., str]],
        **kwargs,
    ) -> None:
        super().__init__(**kwargs, python_callable=self._execute_operator)
        self.paths = paths
        self.output_path = output_path

    def _execute_operator(self, *args, **kwargs):
        merge_sequences(
            resolve_callable(self.paths, *args, **kwargs),
            resolve_callable(self.output_path, *args, **kwargs),
        )