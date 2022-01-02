def transform_mocks(mocks):
    elements = []
    for mock in mocks:
        elements.append(
            {
                "score": mock["score"],
                "element": mock["element"],
                "x": mock["bbox"][0],
                "y": mock["bbox"][1],
                "w": mock["bbox"][2],
                "h": mock["bbox"][3],
            }
        )
    return elements
