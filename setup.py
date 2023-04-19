from setuptools import setup

with open("requirements.txt") as f:
    required = f.read().splitlines()


setup(
    name="llm_oracle",
    version="0.0.0",
    description="",
    url="https://github.com/sshh12/llm_oracle",
    author="Shrivu Shankar",
    license="MIT",
    packages=["llm_oracle"],
    include_package_data=True,
    install_requires=required,
)
