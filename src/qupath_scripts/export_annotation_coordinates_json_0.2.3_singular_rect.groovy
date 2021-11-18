import qupath.lib.images.servers.ImageServer
import qupath.lib.io.GsonTools
boolean prettyPrint = true

import qupath.lib.roi.RectangleROI



def gson = GsonTools.getInstance(prettyPrint)

def imageData = getCurrentImageData()
def scn_name = imageData.getServer().getMetadata().getName()
def outputDir = buildFilePath(PROJECT_BASE_DIR, 'jsons')
mkdirs(outputDir)


def annotations = getAnnotationObjects()

def list_annotation_output =[]

for (annotation in annotations) {
    if (annotation.getROI().getClass() == qupath.lib.roi.RectangleROI)
    list_annotation_output.add(annotation)


}


//print list_annotation_output

// convert annotation data to json obj[0]
def data = gson.toJson(list_annotation_output)

// write file
def out_fp = buildFilePath(outputDir, scn_name + '.json')
File file = new File(out_fp)
new File(out_fp).write(data)
print 'Done!'
print out_fp


