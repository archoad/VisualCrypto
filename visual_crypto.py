#! /usr/bin/env python


import sys, random, string


def readTarga(file):
	print "Lecture de %s" % (file)
	f = open(file, "rb")
	head = f.read(18)
	if ord(head[2]) <> 3:
		print "\n --> L'IMAGE N'EST PAS EN NIVEAU DE GRIS <--\n"
		sys.exit(1)
	width = ord(head[12]) + ord(head[13])*256;
	height = ord(head[14]) + ord(head[15])*256;
	picture = f.read(width*height)
	f.close();
	bitmap = []
	for item in picture:
		bitmap.append(ord(item))
	return head, bitmap


def writeTarga(file, head, bitmap):
	print "Ecriture de %s" % (file)
	file = "result/"+file
	f = open(file, "wb")
	for item in head:
		f.write(item)
	for item in bitmap:
		f.write(chr(item))
	f.close();


def keygen(num):
	key = []
	for i in range(num):
		key.append(random.randint(0,255))
	return key


def keygenPerm(num):
	key = []
	while len(key) < num:
		rand = random.randint(0,num-1)
		if not(rand in key):
			key.append(rand)
	return key


def xor(bitmap, key):
	klen = len(key)
	print "Chiffrement par xor avec cle aleatoire de longueur %d" % (klen)
	n=0
	cipherBitmap = []
	for item in bitmap:
		cipherBitmap.append(item ^ key[n%klen])
		n+=1;
	return cipherBitmap


def vernam(bitmap):
	print "Chiffrement avec masque jetable (Vernam)"
	klen = len(bitmap)
	key = keygen(klen)
	n=0
	cipherBitmap = []
	for item in bitmap:
		cipherBitmap.append(item ^ key[n%klen])
		n+=1
	return cipherBitmap


def cesar(bitmap, decalage):
	print "Chiffrement par substitution monoalphabetique (Cesar), decalage de %d" % (decalage)
	cipherBitmap = []
	for item in bitmap:
		cipherBitmap.append((item + decalage) % 256)
	return cipherBitmap


def cesarTexte(texte, decalage):
	print "Chiffrement par substitution monoalphabetique (Cesar), decalage de %d" % (decalage)
	texte = string.upper(texte)
	cipherTexte = ""
	for ch in texte:
		if ch == ' ':
			cipherTexte = cipherTexte + ch
		else:
			ch = chr((((ord(ch)-65)+decalage)%26)+65)
			cipherTexte = cipherTexte + ch
	return cipherTexte


def cesarCipher(cipher, decalage):
	print "Dechiffrement par substitution monoalphabetique (Cesar), decalage de %d" % (decalage)
	cipher = string.upper(cipher)
	clearTexte = ""
	for ch in cipher:
		if ch == " ":
			clearTexte = clearTexte + ch
		else:
			ch = chr((((ord(ch)-65)-decalage)%26)+65)
			clearTexte = clearTexte + ch
	return clearTexte


def affine(bitmap, a, b):
	print "Chiffrement par substitution affine, clef a: %d, clef b: %d" % (a, b)
	cipherBitmap = []
	for item in bitmap:
		cipherBitmap.append(((a * item) + b) % 256)
	return cipherBitmap


def affineTexte(texte, a, b):
	print "Chiffrement par substitution affine, clef a: %d, clef b: %d" % (a, b)
	texte = string.upper(texte)
	cipherTexte = ""
	for ch in texte:
		if ch == ' ':
			cipherTexte = cipherTexte + ch
		else:
			ch = chr(((((ord(ch)-65)*a)+b)%26)+65)
			cipherTexte = cipherTexte + ch
	return cipherTexte


def vigenere(bitmap, key):
	klen = len(key)
	print "Chiffrement par substitution polyalphabetique (Vigenere), cle de longueur %d" % (klen)
	cipherBitmap = []
	n = 0
	for item in bitmap:
		cipherBitmap.append((item + key[n%klen]) % 256)
		n+=1
	return cipherBitmap


def vigenereTexte(c,k,e=1):
	# e=1 to encrypt, e=-1 to decrypt
	wk=[string.ascii_uppercase.find(ch) for ch in k.upper()]
	wc=[string.ascii_uppercase.find(ch) for ch in c.upper()]
	wc = [ (x[0]+(e*x[1]))%26 for x in zip(wc,wk*(len(wc)/len(wk)+1))]
	return string.join([string.ascii_uppercase[x] for x in wc],"")


def vigenereVideo(head, bitmap, key):
	klen = len(key)
	cipherBitmap, clairBitmap = [], []
	n = 0
	for item in bitmap:
		cipherBitmap.append((item + key[n%klen]) % 256)
		clairBitmap = bitmap[n:]
		if n % 100 == 0:
			writeTarga("chat_vigenere_%s.tga" % (string.zfill(str(n),8)), head, (cipherBitmap + clairBitmap))
		n+=1


def substitution(bitmap, key):
	return vigenere(bitmap, key)


def permutation(bitmap, key):
	print "Chiffrement par permutation avec un clef de longueur %d" % (len(key))
	cipherBitmap, temp, dic, n, cpt = [], [], {}, 0, 0
	for item in bitmap:
		temp.append(item)
		cpt+=1
		if cpt%len(key)==0:
			dic[n] = temp
			temp=[]
			n+=1
	for n in range(len(dic)):
		ligne = dic[n]
		for num in key:
			cipherBitmap.append(ligne[num])
	return cipherBitmap


def permutationTexte(text, key):
	cipherTexte = ""
	text = string.upper(text)
	texteClair = [ord(ch) for ch in text]
	result = permutation(texteClair, key)
	for item in result:
		cipherTexte = cipherTexte + chr(item)
	return cipherTexte


def permutationVideo(head, bitmap, key):
	cipherBitmap, temp, dic, n, cpt = [], [], {}, 0, 0
	for item in bitmap:
		temp.append(item)
		cpt+=1
		if cpt%len(key)==0:
			dic[n] = temp
			temp=[]
			n+=1
	cpt = 1
	for n in range(len(dic)):
		ligne = dic[n]
		for num in key:
			cipherBitmap.append(ligne[num])
			clairBitmap = bitmap[cpt:]
			if cpt % 100 == 0:
				writeTarga("chat_perm_%s.tga" % (string.zfill(str(cpt),8)), head, (cipherBitmap + clairBitmap))
			cpt += 1


def rc4(bitmap, key):
	permutation, j = range(256), 0
	for i in range(256):
		j = ( j + permutation[i] + key[i%len(key)] ) % 256
		permutation[i],permutation[j] = permutation[j],permutation[i]
	i,j,cipherBitmap = 0, 0, []
	for item in bitmap:
		i = (i+1)%256
		j = (j+permutation[i])%256
		permutation[i],permutation[j] = permutation[j],permutation[i]
		k = permutation[(permutation[i]+permutation[j])%256]
		cipherBitmap.append(item^k)
	return cipherBitmap


def rc4Texte(bitmap, key):
	permutation, j = range(256), 0
	for i in range(256):
		j = ( j + permutation[i] + ord(key[i%len(key)]) ) % 256
		permutation[i],permutation[j] = permutation[j],permutation[i]
	i,j,cipherTexte = 0, 0, ""
	for c in bitmap:
		i = (i+1)%256
		j = (j+permutation[i])%256
		permutation[i],permutation[j] = permutation[j],permutation[i]
		k = permutation[(permutation[i]+permutation[j])%256]
		cipherTexte += chr(ord(c)^k)
	return cipherTexte


def rc4Video(head, bitmap, key):
	permutation, j = range(256), 0
	for i in range(256):
		j = ( j + permutation[i] + key[i%len(key)] ) % 256
		permutation[i],permutation[j] = permutation[j],permutation[i]
	i,j,cipherBitmap = 0, 0, []
	cpt = 1
	for item in bitmap:
		i = (i+1)%256
		j = (j+permutation[i])%256
		permutation[i],permutation[j] = permutation[j],permutation[i]
		k = permutation[(permutation[i]+permutation[j])%256]
		cipherBitmap.append(item^k)
		clairBitmap = bitmap[cpt:]
		if cpt % 100 == 0:
			writeTarga("chat_rc4_%s.tga" % (string.zfill(str(cpt),8)), head, (cipherBitmap + clairBitmap))
		cpt += 1


def genCipherFiles(head, bitmap):
	keyA = [1, 40, 100]
	keyB = [0, 40, 100]

	keySubst = []
	keyPerm = []
	print "Generation des clefs de substitution et de permutation"
	for i in [4, 8, 16, 32, 64, 100, 400]:
		keySubst.append(keygen(i))
		keyPerm.append(keygenPerm(i))

#	writeTarga("chat_vernam_%s.tga" % (len(bitmap)), head, vernam(bitmap))

#	for key in [32, 64, 96, 128, 160, 192, 224]:
#		writeTarga("chat_cesar_%d.tga" % (key), head, cesar(bitmap, key))

#	for key_a in keyA:
#		for key_b in keyB:
#			writeTarga("chat_affine_%d_%d.tga" % (key_a,key_b), head, affine(bitmap, key_a, key_b))

#	for key in keySubst:
#		writeTarga("chat_xor_%s.tga" % (len(key)), head, xor(bitmap, key))
#		writeTarga("chat_vigenere_%d.tga" % (len(key)), head, vigenere(bitmap, key))
#		writeTarga("chat_rc4_%d.tga" % len(key), head, rc4(bitmap, key))

#	for key in keyPerm:
#		writeTarga("chat_permutation_%d.tga" % (len(key)), head, permutation(bitmap, key))

	for keyS in keySubst:
		for keyP in keyPerm:
			cipher1 = substitution(bitmap, keyS)
			cipher2 = permutation(cipher1, keyP)
			writeTarga("chat_s%s_p%s.tga" % (len(keyS), len(keyP)), head, cipher2)
#			cipher1 = permutation(bitmap, keyP)
#			cipher2 = substitution(cipher1, keyS)
#			writeTarga("chat_ps_%s.tga" % (len(keyS)), head, cipher2)


def testCrypto(cipher):
	# on imprime le cipher
	print(cipher)
	# calcul de la frequence des lettres du cipher
	alphabet = {"A":0,"B":0,"C":0,"D":0,"E":0,"F":0,"G":0,"H":0,"I":0,"J":0,"K":0,"L":0,"M":0,"N":0,"O":0,"P":0,"Q":0,"R":0,"S":0,"T":0,"U":0,"V":0,"W":0,"X":0,"Y":0,"Z":0}
	cipher = string.upper(cipher)
	for ch in cipher:
		if ch in alphabet:
			alphabet[ch] += 1
	print alphabet
	# Substitution avec la cle
	key = "THALES"
	l = len(key)
	result = ""
	cpt = 0 
	for ch in cipher:
		result = result  + chr( ( (ord(ch) + ord(key[cpt % l]) - 65) % 65 ) + 65 )
		cpt += 1
	print result
	# suppression des espaces
	result = ""
	for ch in cipher:
		if ch != " ":
			result = result + ch
	cipher_ww = result
	print cipher_ww
	# permutations en colonnes
	permut = 5
	result = ""
	cpt = 0
	for ch in cipher_ww:
		print ch, 
		cpt += 1
		if (cpt % permut) == 0:
			print
			cpt = 0
	# inversion du message
	result = ""
	tab, temp = [], []
	cpt = 1
	for i in range(len(cipher_ww)):
		tab.append(cipher_ww[-cpt])
		cpt += 1
	print tab


#Creer un fichier DivX4 a partir de tous les fichiers TGA du repertoire courant:
#	mencoder mf://*.tga -mf w=200:h=200:fps=25:type=tga -ovc xvid -xvidencopts bitrate=1500 -o sortie.avi


# Convert multiples tga files in png:
#	mogrify -format png *.tga

if __name__ == "__main__":
#	testCrypto("LAPIC NIRPE RTNOC NEREC APSE' LAECA FEUTI SDNAT SNOSR USRES SAPAE TIVNI SUOVT EETIR UCESA LEDSE SISSA SEDNO ITIDE ELLEV UONET TECAE UNEVN EIBAL ETIAH UOSSU OVSEL AHT")

	(head, bitmap) = readTarga("chat.tga")
	genCipherFiles(head, bitmap)

#	print cesarTexte("veni vidi vici", 3)
#	for i in range(13):
#		print cesarCipher("LAPIC NIRPE RTNOC NEREC APSE' LAECA FEUTI SDNAT SNOSR USRES SAPAE TIVNI SUOVT EETIR UCESA LEDSE SISSA SEDNO ITIDE ELLEV UONET TECAE UNEVN EIBAL ETIAH UOSSU OVSEL AHT", i)
#	print affineTexte("veni vidi vici", 3, 6)
#	keyTxt = keygenPerm(3)
#	print keyTxt
#	print permutationTexte("veni vidi vici", keyTxt)
#	print vigenereTexte("veni vidi vici", "vigenere")
#	test = rc4Texte('Attack at dawn', 'Secret')
#	print test.encode('hex').upper()

#	vigenereVideo(head, bitmap, keygen(100))
#	rc4Video(head, bitmap, keygen(40))
#	permutationVideo(head, bitmap, keygenPerm(10))
