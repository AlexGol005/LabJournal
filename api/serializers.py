def note_to_json(viscosimeterType):
    return {
        "pairNumber": viscosimeterType.pairNumber,
        "diameter": viscosimeterType.diameter,
        "viscosity1000": viscosimeterType.viscosity1000,
        "range": viscosimeterType.range,
        "type": viscosimeterType.type,
        "intervalVerification": viscosimeterType.intervalVerification,
        "create_at": viscosimeterType.create_at,
        "update_at": viscosimeterType.update_at
    }