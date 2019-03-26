import os

override = input("Do you want to override any existing .cpp files? (You might lose contents of your .cpp files) (Y/N) ")
override = input("Are you sure? (Y/N) ")
override = str.upper(override)

if override.startswith('Y'):
    override = 'w+'
else:
    override = 'a'

for filename in os.listdir():
    if filename.endswith(".h"):
        # Open header file
        header = open(filename, 'r')
        # Opne/create .cpp file
        cpp = open(filename.replace(".h", ".cpp"), override)
        # Add include to .cpp file
        cpp.write('#include "{}"\n\n'.format(filename))

        # some variables
        inClass = 0
        inFunction = 0
        skipOneLine = False
        className = []

        # Checks each line in header
        for line in header:    
            if skipOneLine:
                skipOneLine = False
                continue

            # Removes spacing from each line
            line = line.lstrip()        

            # This string marks end of a class
            if "};" in line:
                inClass -= 1
                className.pop()
        
            # This checks if function has body inside header file
            # and skips over this body
            if line.startswith("{"):
                inFunction += 1
            if line.startswith("}"):
                inFunction -= 1

            # Check if inside a function's body, and skip this line if True
            skipLine = inFunction > 0

            # List of ignore strings that skip over this line
            ignoreStrings = ["//", "#", "public:", "private:", "protected:", "{", "};", "friend"]
            for i in ignoreStrings:
                if i in line:
                    skipLine = True

            # List of required strings in order to create a function from this line
            requiredStrings = ["(", ";"]
            for r in requiredStrings:
                if r not in line:
                    skipLine = True

            # If this line isn't skipped
            if not skipLine:
                # Remove virutal keywords
                function = line.replace("virtual ", "")

                if inClass > 0:
                    # Check of this is constructor/destructor and add className:: to thier names
                    if function.startswith("operator") or function.replace("~", "").startswith(className[-1]):
                        function = "{}::".format(className[-1]) + function
                    # Else add className:: before function's name which should be right after first whitespace
                    else:
                        function = line.replace("virtual ", "")
                        function = function.replace(" ", " {}::".format(className[-1]), 1)
                
                # Replace semicolon ; with empty body of a function
                function = function.replace(";", "\n{\n\n}\n")

                # Write function to .cpp file
                cpp.write(function)
            
            # If class/struct string is in line extract it's name and append it to className list
            # and in next iteration start looking for class/struct functions
            if "class " in line:
                inClass += 1
                className.append(line.split("class ")[1].split(":")[0].rstrip())
                className[-1] = className[-1].replace("\n", "")
                skipOneLine = True            
            if "struct " in line:
                inClass += 1
                className.append(line.split("struct ")[1].split(":")[0].rstrip())
                className[-1] = className[-1].replace("\n", "")
                skipOneLine = True

            # This is only here because I'm lazy, but hey whatever works
            if "enum " in line:
                inClass += 1
                className.append(line.split("enum ")[1].split(":")[0].rstrip())
                className[-1] = className[-1].replace("\n", "")
                skipOneLine = True