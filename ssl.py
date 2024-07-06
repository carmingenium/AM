import ssl
context = ssl._create_unverified_context()
urllib.request.urlopen(req,context=context)


  # fix-ssl:
  #   runs-on: self-hosted
  #   steps:
  #     - name: Set up Python
  #       uses: actions/setup-python@v4
  #       with:
  #         python-version: '3.12'
  #     - name: Install dependencies
  #     - name: Run SSL code
  #       run:
  #         python ssl.py