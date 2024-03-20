DIGITS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

def KMPSearch(pat, txt):
    ind = []
    M = len(pat)
    N = len(txt)

    # create lps[] that will hold the longest prefix suffix
    # values for pattern
    lps = [0]*M
    j = 0  # index for pat[]

    # Preprocess the pattern (calculate lps[] array)
    computeLPSArray(pat, M, lps)

    i = 0  # index for txt[]
    while (N - i) >= (M - j):
        if pat[j] == txt[i]:
            i += 1
            j += 1

        if j == M:
            ind.append(i-j)
            j = lps[j-1]

        # mismatch after j matches
        elif i < N and pat[j] != txt[i]:
            # Do not match lps[0..lps[j-1]] characters,
            # they will match anyway
            if j != 0:
                j = lps[j-1]
            else:
                i += 1
    
    if len(ind) == 0:
        return -1, -1
    elif len(ind) == 1:
        return ind[0], ind[0]
    else:    
        return ind[0], ind[len(ind) - 1]


# Function to compute LPS array
def computeLPSArray(pat, M, lps):
	len = 0 # length of the previous longest prefix suffix

	lps[0] = 0 # lps[0] is always 0
	i = 1

	# the loop calculates lps[i] for i = 1 to M-1
	while i < M:
		if pat[i] == pat[len]:
			len += 1
			lps[i] = len
			i += 1
		else:
			# This is tricky. Consider the example.
			# AAACAAAA and i = 7. The idea is similar
			# to search step.
			if len != 0:
				len = lps[len-1]

				# Also, note that we do not increment i here
			else:
				lps[i] = 0
				i += 1

def sum(inputs):
    sum = 0
    for input in inputs:
        num = num_from_string(input)
        sum += num
    return sum

def word_num_from_string(string):
    minfp = len(string)
    fd = None
    maxlp = 0
    ld = None
    i = 1
    for digit in DIGITS:
        fp, lp = KMPSearch(digit, string)
        if fp != -1 and fp <= minfp:
            minfp = fp
            fd = i
        if lp != -1 and lp >= maxlp:
            maxlp = lp
            ld = i
        i += 1
    return (fd, minfp), (ld, maxlp)

def digit_num_from_string(string):
    f = (None, -1)
    l = (None, -1)
    num = 0
    digit = -1
    pos = 0
    i = 0
    for c in string:
        if c.isdigit():
            digit = int(c)
            if pos == 0:
                f = (digit, i)
            l = (digit, i)
            pos += 1
        i += 1
    
    return f, l

def num_from_string(string):
    num = 0
    (wf, wfp), (wl, wlp) = word_num_from_string(string)
    (df, dfp), (dl, dlp) = digit_num_from_string(string)
    
    d = []
    p = []
    
    if wf != None:
        d.append(wf)
        p.append(wfp)
    if wl != None:
        d.append(wl)
        p.append(wlp)
    if df != None:
        d.append(df)
        p.append(dfp)
    if dl != None:
        d.append(dl)
        p.append(dlp)
        
    #print(f"d={d}")
    #print(f"p={p}")
    
    min = len(string)
    f = None
    max = 0
    l = None
    for i in range(len(d)):
        if p[i] <= min:
            min = p[i]
            f = d[i]
        if p[i] >= max:
            max = p[i]
            l = d[i]
    
    return f * 10 + l

if __name__ == '__main__':
    inputs = []
    with open('input1.txt', 'r') as file:
        for line in file:
            line = line.strip()
            inputs.append(line)
    
    #n = num_from_string("3eighteightllkbxkbs9zgznxtj8lfflcst")     
    #print(f"n={n}")
    print(f"Input size: {len(inputs)}")
    print(f"Sum is: {sum(inputs)}")