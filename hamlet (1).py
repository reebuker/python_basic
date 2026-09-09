import re
from english_stopwords import stopwords

with open('./hamlet.txt') as f:
    hamlet = f.read()

for stopword in stopwords:
    hamlet = re.sub(
        r'[\s\W]+(' + stopword + r')[\s\W]+', 'DELETED ', hamlet, flags=re.IGNORECASE
    )

hamlet = re.sub(
        r'DELETED', '[DELETED]', hamlet, flags=re.IGNORECASE
)

with open('./hamlet_no_stopwords.txt', 'w') as f:
    f.write(hamlet.strip())