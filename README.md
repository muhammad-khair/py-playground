# Python Experimentation

## Background

This repository experiments with the following:
- quickfix (under `src`)
- advanced python concepts (under `test/unit`)
  - *args and **kwargs
  - abc (as interfaces)
  - decorators
  - iterators
- robot framework (under `test/robot`)

There is also CI workflows implemented (in `.github/workflows`).

## Usage

### Setup

Setup a virtual environment and install required dependencies.

```bash
$ python3 -m venv venv
$ source venv/bin/activate

# you have entered venv
(venv) $
(venv) $ export PYTHONPATH=$(pwd)
(venv) $ python -m pip install --upgrade pip
(venv) $ pip install -r requirements.txt
```

If you face issues installing `quickfix-1.15.1`, and you need a local instance of it, you can:
1. Install the package manually into your local space, place it under `<project-dir>/lib/quickfix-1.15.1`.
   - This directory will be ignored by `.gitignore`.
2. Make changes in the package so that it can work to your local environment needs.
   - This requires some googling based on your device.
3. Create a `local-requirements.txt` with the `quickfix` dependency pointing to your **absolute** path of your new package.
   ```bash
   # local-requirements.txt
   quickfix @ file:///Users/user/my-repo/lib/quickfix-1.15.1
   pytest == 8.2.2
   robotframework == 7.0.1
   ```
   - Local path will not be recognised by `pip`.
   - This file will also be ignored by `.gitignore`.
4. Rerun your installation command once again but now with `local-requirements.txt`.
   ```bash
   (venv) $ pip install -r local-requirements.txt
   ```

Once you are done using the virtual environment, you can deactivate it.

```bash
(venv) $ unset PYTHONPATH
(venv) $ deactivate

# you have left venv
$
```

You can also modify `venv/bin/activate` script to `export` and `unset` variable `PYTHONPATH` to save time for future reboots.

### Quickfix

Run the server and client on separate terminals.

```bash
# Run server in one terminal first
(venv) $ python src/server.py
onCreate : Session (FIX.4.3:SERVER->CLIENT)
(Admin) R << 8=FIX.4.3|9=73|35=A|34=1|49=CLIENT|52=20240714-18:18:10.000|56=SERVER|98=0|108=30|141=Y|10=185|
(Admin) S >> 8=FIX.4.3|9=73|35=A|34=1|49=SERVER|52=20240714-18:18:10.000|56=CLIENT|98=0|108=30|141=Y|10=185|
Successful Logon to session 'FIX.4.3:SERVER->CLIENT'.
```

```bash
# Run client in a separate terminal next
(venv) $ python src/client.py
onCreate : Session (FIX.4.3:CLIENT->SERVER)
Please choose 1 for Put New Order or 2 for Exit!
(Admin) S >> 8=FIX.4.3|9=73|35=A|34=1|49=CLIENT|52=20240714-18:18:10.000|56=SERVER|98=0|108=30|141=Y|10=185|
(Admin) R << 8=FIX.4.3|9=73|35=A|34=1|49=SERVER|52=20240714-18:18:10.000|56=CLIENT|98=0|108=30|141=Y|10=185|
Successful Logon to session 'FIX.4.3:CLIENT->SERVE
```

### Unit tests

Run unit tests with pytests.

```bash
(venv) $ python -m pytest test/unit -v --junitxml=reports/pytest.xml
============================ test session starts =============================
...
```

### Robot tests

Run robot tests.

```bash
(venv) $ robot --outputdir reports/robot test/robot
==============================================================================
Robot                                                                         
==============================================================================
Robot.Keyword Driven :: Example test cases using the keyword-driven testing...
==============================================================================
...
```
