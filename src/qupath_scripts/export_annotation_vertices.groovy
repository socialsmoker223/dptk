// Create an empty text file

def name = getProjectEntry().getImageName() + '.txt'
def path = buildFilePath(PROJECT_BASE_DIR, 'vertices')
mkdirs(path)
path = buildFilePath(path, name)


def file = new File(path)
file.text = ''

// Loop through all objects & write the points to the file
for (pathObject in getAllObjects()) {
    // Check for interrupt (Run -> Kill running script)
    if (Thread.interrupted())
        break
    // Get the ROI
    def roi = pathObject.getROI()
    def class_ = pathObject.getName()
    if (roi == null)
        continue
    // Write the points; but beware areas, and also ellipses!
    file << "Class:" << class_ << roi.getPolygonPoints() << System.lineSeparator()
}
print 'Done!'