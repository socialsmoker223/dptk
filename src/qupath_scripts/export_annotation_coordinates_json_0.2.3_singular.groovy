import qupath.lib.images.servers.ImageServer
import qupath.lib.io.GsonTools
boolean prettyPrint = true


def gson = GsonTools.getInstance(prettyPrint)

def imageData = getCurrentImageData()
def scn_name = imageData.getServer().getMetadata().getName()
def outputDir = buildFilePath(PROJECT_BASE_DIR, 'jsons')
mkdirs(outputDir)


def annotations = getAnnotationObjects()
// convert annotation data to json obj
def data = gson.toJson(annotations)

// write file
def out_fp = buildFilePath(outputDir, scn_name + '.json')
File file = new File(out_fp)
new File(out_fp).write(data)
print 'Done!'
print out_fp



// convert annotation data to json obj
//def data = gson.toJson(annotations)
