import bgznewcontributors
import pickle
import sys

release = int(sys.argv[1])
data = bgznewcontributors.get_new_assignees(["Firefox %i" % (release), "mozilla%i" % (release)])
f = open(sys.argv[2], "wb")
pickle.dump(data, f)
f.close()
