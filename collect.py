import re, glob
import hou, os, shutil

# Main function
def BackupAllContent(inputpath):
    backpath = os.path.join(hou.expandString(inputpath), os.path.splitext(os.path.basename(hou.hipFile.name()))[0], "")
    subch = hou.node("/").allSubChildren()
    for child in subch:
        parms_in_nodes = child.parms()
        for parm in parms_in_nodes:
            if parm.parmTemplate().type() == hou.parmTemplateType.String:
                syc_test = ""
                try:
                    syc_test = glob.glob(hou.expandString(re.sub(r'\$F\d', "*", parm.unexpandedString())))[0]
                except:
                    pass
                if os.path.exists(syc_test) and parm.eval() != "*":
                    fl_to_copy = os.path.splitext(parm.eval())[1].replace(".", "") + ("" if not re.search(r".\d+\D*$", parm.eval()) else "/" + re.sub(r'.\d+\D*$', '', os.path.split(parm.eval())[1]))
                    newpath = backpath + fl_to_copy
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
                    files = glob.glob(hou.expandString(re.sub(r'\$F\d', "*", parm.unexpandedString())))
                    for fls in files:
                        if not os.path.exists(os.path.join(newpath, os.path.basename(fls))):
                            shutil.copy(fls, newpath)
                    path_to_imp = os.path.join("$HIP/", fl_to_copy, os.path.split(parm.unexpandedString())[1])
                    parm.set(path_to_imp)
    hipN = backpath + os.path.basename(hou.hipFile.name())
    hou.hipFile.save(hipN)


# Create dialog and execute function
# You can add this line to shell for quck access
backpath = hou.ui.selectFile(title="Select Directory to Backup", file_type=hou.fileType.Directory)
if backpath != "":
    BackupAllContent(backpath)
    hou.ui.displayMessage("Your Project has been Baked Successfully to:\n" + hou.hipFile.name())
else:
    hou.ui.displayMessage("You have canceled or chosen wrong Directory, try again:\n" + hou.hipFile.name())
