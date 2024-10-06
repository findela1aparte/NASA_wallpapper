import os
import platform

so = os.name
plataforma= platform.platform(aliased=0, terse=0)

print (so)
print (plataforma)

if so == "posix":
    print("Tu sistema operativo es Unix, más concretamente " + plataforma )
elif so == "nt":
    print("Tu sistema operativo es Windows")
elif so == "mac":
    print("Tu sistema operativo es Mac")  

#Comentario  
