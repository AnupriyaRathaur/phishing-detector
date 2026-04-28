from collections import defaultdict

# Global stats storage
stats = {
    "total": 0,
    "labels": defaultdict(int),
    "tlds": defaultdict(int)
}

# Update stats after each prediction
def update_stats(domain, label):
    stats["total"] += 1
    stats["labels"][label] += 1

    # Extract TLD
    try:
        tld = domain.split('.')[-1]
        stats["tlds"][tld] += 1
    except:
        pass


# Get stats summary
def get_stats():
    return {
        "total_domains": stats["total"],
        "count_per_label": dict(stats["labels"]),
        "top_risky_tlds": sorted(
            stats["tlds"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
    }