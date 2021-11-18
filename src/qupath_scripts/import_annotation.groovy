// this image
// load all jsons
// for each json , if image name in json file name
// import annotation

import com.google.gson.Gson
import qupath.lib.geom.Point2
import qupath.lib.objects.PathAnnotationObject
import qupath.lib.roi.PolygonROI
import groovy.io.FileType

// ----------------FILE IO ------------------- //

input_dir = "predictions"

// Get the current image (supports 'Run for project')
def imageData = getCurrentImageData()

// Define output path (here, relative to project)
def slide_name = GeneralTools.getNameWithoutExtension(imageData.getServer().getMetadata().getName())

def json_list = []
def dir = new File(input_dir)
dir.eachFileRecurse (FileType.FILES) { file ->
  json_list << file
}



for (i in json_list) {

    String json_file_path = i

    if (json_file_path.contains(slide_name)) {

        print("Found annotation file for :")
        print(slide_name)

        // ----------------IMPORT------------------- //


        // file_path = "prediction_21Y08519 -2.svs.json"

        def myjson = new File(json_file_path).text

        // Read into a map
        def map = new Gson().fromJson(myjson, Map)

        // Extract tumor & annotations
        def tumorAnnotations = map['tumor']
        def stromaAnnotations = map['stroma']
        def otherAnnotations = map['other']

        def tumor_class = getPathClass('Tumor')
        def stroma_class = getPathClass('Stroma')
        def other_class = getPathClass('Other')

        all_annotation_class = [tumorAnnotations, stromaAnnotations, otherAnnotations]

        // Convert to QuPath annotations
        def annotations = []
        for (class_annotation in all_annotation_class) {

            for (annotation in class_annotation) {

                def name = annotation['name']
                def vertices = annotation['vertices']
                def points = vertices.collect {new Point2(it[0], it[1])}
                def polygon = new PolygonROI(points)

                // # create annotation object
                def pathAnnotation = new PathAnnotationObject(polygon)
                pathAnnotation.setName(name)

                if (name.contains("tumor"))
                    pathAnnotation.setPathClass(tumor_class)
                else if(name.contains("stroma"))
                    pathAnnotation.setPathClass(stroma_class)
                else if(name.contains("other"))
                    pathAnnotation.setPathClass(other_class)

                annotations << pathAnnotation
            }
        }



        //Add to current hierarchy
        QPEx.addObjects(annotations)


    }
    else {
    print("Unabel to find annotation for this slide")
    }
}

