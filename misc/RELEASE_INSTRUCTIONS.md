## One time setup ( per host/environment) ##
### PYPI Test ###
- add repository to poetry config: `poetry config repositories.audio-program-generator https://test.pypi.org/legacy/`
- get token from https://test.pypi.org/manage/account/token/
- store token using poetry config pypi-token.test-pypi  pypi-YYYYYYYY
### PYPI Production ###
- get token from https://pypi.org/manage/account/token/
- store token using poetry config pypi-token.pypi pypi-XXXXXXXX

## Each time you need to publish ##
### Bump version ###
- poetry version prerelease or
- poetry version patch

## Poetry Publish ##
### To TestPyPi ###
 - poetry publish -r test-pypi
### To PyPi ###
- poetry publish
