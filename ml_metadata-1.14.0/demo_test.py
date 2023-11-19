from pprint import pprint

import ml_metadata as mlmd
from ml_metadata.metadata_store import metadata_store
from ml_metadata.proto import metadata_store_pb2

def test_demo():
    # Setup client config
    client_connection_config = metadata_store_pb2.MetadataStoreClientConfig()
    client_connection_config.host = 'localhost'
    client_connection_config.port = 8080

    store = metadata_store.MetadataStore(client_connection_config)
    
    # Create ArtifactTypes, e.g., DataSet
    data_type = metadata_store_pb2.ArtifactType()
    data_type.name = "DataSet"
    data_type.properties["day"] = metadata_store_pb2.INT
    data_type.properties["split"] = metadata_store_pb2.STRING
    data_type_id = store.put_artifact_type(data_type)
    pprint(data_type_id)

    # Create ArtifactTypes, e.g.,SavedModel
    model_type = metadata_store_pb2.ArtifactType()
    model_type.name = "SavedModel"
    model_type.properties["version"] = metadata_store_pb2.INT
    model_type.properties["name"] = metadata_store_pb2.STRING
    model_type_id = store.put_artifact_type(model_type)
    pprint(model_type_id)

    # ModelVersion
    model_version_type = metadata_store_pb2.ContextType()
    model_version_type.name = "odh.ModelVersion"
    model_version_type.properties["model_name"] = metadata_store_pb2.STRING
    model_version_type.properties["version"] = metadata_store_pb2.STRING
    model_version_type_id = store.put_context_type(model_version_type)
    pprint(model_version_type_id)

    # Query all registered Artifact types.
    artifact_types = store.get_artifact_types()
    pprint(artifact_types)

    # Create an ExecutionType, e.g., Trainer
    trainer_type = metadata_store_pb2.ExecutionType()
    trainer_type.name = "Trainer"
    trainer_type.properties["state"] = metadata_store_pb2.STRING
    trainer_type_id = store.put_execution_type(trainer_type)
    pprint(trainer_type_id)

    # Query a registered Execution type with the returned id
    [registered_type] = store.get_execution_types_by_id([trainer_type_id])
    pprint(registered_type)
    
    # Create an input artifact of type DataSet
    data_artifact = metadata_store_pb2.Artifact()
    data_artifact.uri = 'path/to/data'
    data_artifact.properties["day"].int_value = 1
    data_artifact.properties["split"].string_value = 'train'
    data_artifact.type_id = data_type_id
    [data_artifact_id] = store.put_artifacts([data_artifact])
    pprint(data_artifact_id)

    # Query all registered Artifacts
    artifacts = store.get_artifacts()
    pprint(artifacts)

    # Plus, there are many ways to query the same Artifact
    [stored_data_artifact] = store.get_artifacts_by_id([data_artifact_id])
    print(stored_data_artifact)
    artifacts_with_uri = store.get_artifacts_by_uri(data_artifact.uri)
    pprint(artifacts_with_uri)

    artifacts_with_conditions = store.get_artifacts(
        list_options=mlmd.ListOptions(
            filter_query='uri LIKE "%/data" AND properties.day.int_value > 0'))
    pprint(artifacts_with_conditions)

    # Register the Execution of a Trainer run
    trainer_run = metadata_store_pb2.Execution()
    trainer_run.type_id = trainer_type_id
    trainer_run.properties["state"].string_value = "RUNNING"
    [run_id] = store.put_executions([trainer_run])
    pprint(run_id)

    # Query all registered Execution
    executions = store.get_executions_by_id([run_id])
    pprint(executions)

    # Similarly, the same execution can be queried with conditions.
    executions_with_conditions = store.get_executions(
        list_options = mlmd.ListOptions(
            filter_query='type = "Trainer" AND properties.state.string_value IS NOT NULL'))
    pprint(executions_with_conditions)
    
    # Define the input event
    input_event = metadata_store_pb2.Event()
    input_event.artifact_id = data_artifact_id
    input_event.execution_id = run_id
    input_event.type = metadata_store_pb2.Event.DECLARED_INPUT

    # Record the input event in the metadata store
    store.put_events([input_event])
    # Declare the output artifact of type SavedModel
    model_artifact = metadata_store_pb2.Artifact()
    model_artifact.uri = 'path/to/model/file'
    model_artifact.properties["version"].int_value = 1
    model_artifact.properties["name"].string_value = 'MNIST-v1'
    model_artifact.type_id = model_type_id
    [model_artifact_id] = store.put_artifacts([model_artifact])
    pprint(model_artifact_id)

    # Declare the output event
    output_event = metadata_store_pb2.Event()
    output_event.artifact_id = model_artifact_id
    output_event.execution_id = run_id
    output_event.type = metadata_store_pb2.Event.DECLARED_OUTPUT

    # Submit output event to the Metadata Store
    store.put_events([output_event])
    trainer_run.id = run_id
    trainer_run.properties["state"].string_value = "COMPLETED"
    store.put_executions([trainer_run])

    # Create a ContextType, e.g., Experiment with a note property
    experiment_type = metadata_store_pb2.ContextType()
    experiment_type.name = "Experiment"
    experiment_type.properties["note"] = metadata_store_pb2.STRING
    experiment_type_id = store.put_context_type(experiment_type)

    # Group the model and the trainer run to an experiment.
    my_experiment = metadata_store_pb2.Context()
    my_experiment.type_id = experiment_type_id
    # Give the experiment a name
    my_experiment.name = "exp1"
    my_experiment.properties["note"].string_value = "My first experiment."
    [experiment_id] = store.put_contexts([my_experiment])

    attribution = metadata_store_pb2.Attribution()
    attribution.artifact_id = model_artifact_id
    attribution.context_id = experiment_id

    association = metadata_store_pb2.Association()
    association.execution_id = run_id
    association.context_id = experiment_id

    store.put_attributions_and_associations([attribution], [association])

    # Query the Artifacts and Executions that are linked to the Context.
    experiment_artifacts = store.get_artifacts_by_context(experiment_id)
    pprint(experiment_artifacts)
    experiment_executions = store.get_executions_by_context(experiment_id)
    pprint(experiment_executions)

    # You can also use neighborhood queries to fetch these artifacts and executions
    # with conditions.
    experiment_artifacts_with_conditions = store.get_artifacts(
        list_options = mlmd.ListOptions(
            filter_query=('contexts_a.type = "Experiment" AND contexts_a.name = "exp1"')))
    pprint(experiment_artifacts_with_conditions)
    experiment_executions_with_conditions = store.get_executions(
        list_options = mlmd.ListOptions(
            filter_query=('contexts_a.id = {}'.format(experiment_id))))
    pprint(experiment_executions_with_conditions)
