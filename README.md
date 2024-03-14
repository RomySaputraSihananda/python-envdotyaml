# python-envdotyaml

python-envdotyaml reads the yaml syntax from the env.yaml file and can set it as an environment variable. It helps in developing applications like python-dotenv.

## Getting Started

```bash
pip install python-envdotyaml
```

## Example Usage

```python
import os

from envdotyaml import load_envdotyaml

load_envdotyaml()

print(os.environ)
```

## Example env.yaml

```yaml
AUTH:
  USERNAME: "romy"
  PASSWORD: "V20wNWVXUkhWbnBrUjJ4MVduZHZQUW89Cg=="
```

## Output

```bash
environ(
    {
        'AUTH_USERNAME': 'romy',
        'AUTH_PASSWORD': 'V20wNWVXUkhWbnBrUjJ4MVduZHZQUW89Cg=='
    }
)
```
