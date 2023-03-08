docker_compose('dev/docker-compose.yaml')

sync_pyproj_toml = sync('./pyproject.toml', '/usr/local/airflow/astro_sdk_template/pyproject.toml')
sync_readme = sync('./README.md', '/usr/local/airflow/astro_sdk_template/README.md')
sync_src = sync('./src', '/usr/local/airflow/astro_sdk_template/src')
sync_dev_dir = sync('./src', '/usr/local/airflow/astro_sdk_template/dev')

docker_build(
    'astro-sdk-template-dev',
    context='.',
    dockerfile='dev/Dockerfile',
    only=[
        'dev',
        'pyproject.toml',
        'README.md',
        'src'
    ],
    ignore=[
        'dev/logs',
        'dev/dags'
    ],
    live_update=[
        sync_pyproj_toml,
        sync_src,
        sync_readme,
        sync_dev_dir,
        run(
            'cd /usr/local/airflow/astro_sdk_template && pip install -e .',
            trigger=['pyproject.toml']
        ),
    ]
)
