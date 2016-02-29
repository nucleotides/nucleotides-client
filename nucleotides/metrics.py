def map_cgroup_values(a):
    return {"max_resident_set_size" : a["memory_stats"]["stats"]["rss"],
            "max_cpu_usage"         : a["cpu_stats"]["cpu_usage"]["total_usage"]}

# http://stackoverflow.com/a/25658642/91144
def max_values(a, b):
    return {key:max(value,b[key]) for key, value in a.iteritems() }

def parse_runtime_metrics(metrics):
    return reduce(max_values, map(map_cgroup_values, metrics))
