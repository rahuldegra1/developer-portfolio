def groupAnagram(self, strs):
    groups = {}
    for words in strs:
        key = "".join(sorted(words))
        if key in groups:
            groups[key].append(words)
        else:
            groups[key] = [words]
    return list(groups.values())
