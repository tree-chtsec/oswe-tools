# Utilities

## parallel.py

Very efficient multi-threading API.

### Rough benchmark

Total: 20000 rounds.

**4** threads, complete 2669 rounds in 6 min 13 sec

Avg. 7.1 rounds per sec

```python
parallel.run(__try, range(50000, 70000), verb=True, thread_num=4)
```

![](images/4thread.png)

**128** thread

complete 16539 rounds in 3 min 7 sec

Avg. 88.4 rounds per sec

```python
parallel.run(__try, range(50000, 70000), verb=True, thread_num=128)
```

![](images/128thread.png)

