src = [300, 2, 12, 44, 1, 1, 4, 10, 7, 1, 78, 123, 55]
result = [src[idx] for idx in range(1, len(src)) if src[idx] > src[idx - 1]]
print(result)