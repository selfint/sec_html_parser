# SEC HTML parser

SEC documents aren't formatted in a way that is easy for computers to understand. The
purpose of this library is to take the unstructured format of the SEC documents (e.g.
10K annual report forms) and convert them into a JSON format.

## Examples

The module can also be executed like so:

```sh
$ python -m sec_html_parser /path/to/10k/form.html -o /path/to/output.json
```
