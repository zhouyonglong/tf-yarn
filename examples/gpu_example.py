import logging
import os
from functools import partial

import linear_classifier_experiment as experiment_fn
import winequality

from tf_yarn import run_on_yarn, TaskFlavor, TaskSpec

if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    winequality.ensure_dataset_on_hdfs()
    dataset_path = winequality.get_dataset_hdfs_path()

    run_on_yarn(
        partial(experiment_fn.get, dataset_path),
        task_specs={
            "chief": TaskSpec(memory=2 * 2 ** 10, vcores=4, flavor=TaskFlavor.GPU),
            "evaluator": TaskSpec(memory=2 ** 10, vcores=1)
        },
        files={
            os.path.basename(winequality.__file__): winequality.__file__,
            os.path.basename(experiment_fn.__file__): experiment_fn.__file__,
        },
        queue="ml-gpu"
    )
