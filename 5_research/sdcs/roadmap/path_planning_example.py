import numpy as np
from hal.products.mats import SDCSRoadMap
import matplotlib.image as mpimg
import os

def main():
    # Configuration parameters for example script.
    useSmallMap = False
    leftHandTraffic = True
    nodeSequence = []

    # Create a SDCSRoadMap instance with desired configuration.
    roadmap = SDCSRoadMap(
        leftHandTraffic=leftHandTraffic,
        useSmallMap=useSmallMap
    )

    # Generate the shortest path passing through the given sequence of nodes.
    # - nodeSequence can be a list or tuple of node indicies.
    # - The generated path takes the form of a 2xn numpy array
    path = roadmap.generate_path(nodeSequence=nodeSequence)

    # Print out the location of each node
    for i, node in enumerate(roadmap.nodes):
        print(
            'Node ' + str(i) + ': Pose = ['
            + str(node.pose[0, 0]) + ', '
            + str(node.pose[1 ,0]) + ', '
            + str(node.pose[2, 0]) + ']'
        )

    # Display the roadmap with nodes, edges, and labels using matplotlib.
    plt, ax = roadmap.display()

    # Add the SDCS mats as a background image to the plot generated by display.
    if useSmallMap:
        imgFile = './SDCS_SmallMapLayout.png'
        yOrigin = 299.5
    else:
        imgFile = './SDCS_MapLayout.png'
        yOrigin = 1008.5

    imgPath = os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            imgFile
        )
    )
    img = mpimg.imread(imgPath)
    img = np.flipud(img)
    scale = 0.00476556
    x_translation, y_translation = -483.5 * scale, (yOrigin-img.shape[0]) * scale
    img_extent = (
        x_translation, img.shape[1] * scale + x_translation,
        y_translation, img.shape[0] * scale + y_translation
    )
    ax.imshow(img, extent=img_extent, origin='lower', zorder=0)

    # Plot the generated path, if one exists
    if path is None:
        print('failed to find path')
    else:
        ax.plot(path[0, :], path[1, :], 'red', linestyle='-', linewidth=2)

    plt.show()


if __name__ == '__main__':
    main()
