## kubeslack
A simple python script for basic kubnernetes pod status notifications.

### Usage
See the charts dir for a simple k8s deployment yaml file and service-account permissions

#### Parameters (environment variables)

| Parameter         |      Description   | Example Value  |  Default value |
|-------------------|--------------------|----------------|----------------|
| `SLACK_TOKEN`     | Bot token for slack app, see slack docs for details | `xobo-xxx-xxx-xxx` |  None |
| `SLACK_CHANNEL`   | Slack channel name. The channel needs to exist and the bot needs to be added to the channel |`#k8s` |  None |
| `NAMESPACE`       | The namespace to monitor ('default' if none specified) | `default` | `default` |
| `LOG_LEVEL`       | configure the logging level (logs all namespace events in INFO, regardless if sending to slack) | `WARNING` | `INFO` |
| `TEST`            | If exists reads permissions from .kube/config file (useful for local development). Else uses in-cluster permissions (taken from the service account) | `true` | None |

