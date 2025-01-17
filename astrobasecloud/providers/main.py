import json
from typing import Dict, List

import requests
import typer

from astrobasecloud.cli.config import AstrobaseCLIConfig
from astrobasecloud.types.aws import EKSCluster
from astrobasecloud.types.gcp import GCPSetupSpec, GKECluster
from astrobasecloud.types.provider import ProviderName


class AstrobaseGCPClient:
    def __init__(self) -> None:
        ab_config = AstrobaseCLIConfig()
        self.url = ab_config.current_profile().url()

    def _echo_response(self, data: object) -> None:
        typer.echo(json.dumps(data, indent=2))

    def create_cluster(self, cluster_spec: GKECluster) -> None:
        res = requests.post(
            f"{self.url}/{ProviderName.gcp}/cluster",
            json=json.loads(cluster_spec.json()),
        )
        self._echo_response(res.json())

    def delete_cluster(self, cluster_name: str, project_id: str, location: str) -> None:
        res = requests.delete(
            f"{self.url}/{ProviderName.gcp}/cluster/{cluster_name}"
            f"?project_id={project_id}&location={location}",
        )
        self._echo_response(res.json())

    def setup_provider(self, setup_spec: GCPSetupSpec) -> None:
        res = requests.post(
            f"{self.url}/{ProviderName.gcp}/setup",
            json=json.loads(setup_spec.json()),
        )
        self._echo_response(res.json())


class AstrobaseAWSClient:
    def __init__(self) -> None:
        ab_config = AstrobaseCLIConfig()
        self.url = ab_config.current_profile().url()

    def _echo_response(self, data: object) -> None:
        typer.echo(json.dumps(data, indent=2))

    def create_cluster(self, cluster_spec: EKSCluster) -> None:
        res = requests.post(
            f"{self.url}/{ProviderName.aws}/cluster",
            json=cluster_spec,
        )
        self._echo_response(res.json())

    def delete_cluster(
        self, cluster_name: str, nodegroup_names: List[str], region: str
    ) -> None:
        res = requests.delete(
            f"{self.url}/{ProviderName.aws}/cluster/{cluster_name}"
            f"?region={region}&nodegroup_names={','.join(nodegroup_names)}",
        )
        self._echo_response(res.json())


class AstrobaseAzureClient:
    def __init__(self) -> None:
        ab_config = AstrobaseCLIConfig()
        self.url = ab_config.current_profile().url()

    def _echo_response(self, data: object) -> None:
        typer.echo(json.dumps(data, indent=2))

    def create_cluster(self, cluster_spec: Dict) -> None:
        res = requests.post(
            f"{self.url}/{ProviderName.azure}/cluster",
            json=cluster_spec,
        )
        self._echo_response(res.json())

    def delete_cluster(self, cluster_name: str, resource_group_name: str) -> None:
        res = requests.delete(
            f"{self.url}/{ProviderName.azure}/cluster/{cluster_name}"
            f"?resource_group_name={resource_group_name}",
        )
        self._echo_response(res.json())
