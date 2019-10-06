import md5

m = md5.new()
m.update('qweettttt')

print(m.hexdigest())

m = md5.new()
m.update('qweetttttfgegeggrgrrw   ')

print(m.hexdigest())
