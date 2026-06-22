# SPDX-License-Identifier: GPL-2.0-or-later

bl_info = {
    "name": "火焰燃烧效果",
    "author": "OpenAI",
    "version": (1, 1, 0),
    "blender": (4, 3, 0),
    "location": "3D视图 > 侧栏 > 火焰",
    "description": "创建参考火焰或火焰烟雾效果、紊流并烘焙流体数据",
    "category": "Object",
}

import bpy


FLOW_SETTINGS = {
    "density": 1.0,
    "smoke_color": (0.7, 0.7, 0.7),
    "fuel_amount": 2.0,
    "temperature": 1.0,
    "flow_type": "FIRE",
    "flow_behavior": "INFLOW",
    "flow_source": "MESH",
    "use_absolute": True,
    "use_initial_velocity": False,
    "velocity_factor": 1.0,
    "velocity_normal": 0.0,
    "velocity_random": 0.0,
    "velocity_coord": (0.0, 0.0, 0.0),
    "volume_density": 0.0,
    "surface_distance": 1.0,
    "use_plane_init": False,
    "particle_size": 1.0,
    "use_particle_size": True,
    "use_inflow": True,
    "subframes": 0,
    "density_vertex_group": "",
    "use_texture": True,
    "texture_map_type": "AUTO",
    "uv_layer": "",
    "texture_size": 1.0,
    "texture_offset": 0.0,
}


DOMAIN_SETTINGS = {
    "additional_res": 0,
    "adapt_margin": 4,
    "adapt_threshold": 0.002,
    "use_adaptive_domain": True,
    "resolution_max": 256,
    "use_collision_border_front": False,
    "use_collision_border_back": False,
    "use_collision_border_right": False,
    "use_collision_border_left": False,
    "use_collision_border_top": False,
    "use_collision_border_bottom": False,
    "domain_type": "GAS",
    "delete_in_obstacle": False,
    "alpha": 1.0,
    "beta": 1.0,
    "dissolve_speed": 5,
    "vorticity": 0.0,
    "highres_sampling": "FULLSAMPLE",
    "use_dissolve_smoke": False,
    "use_dissolve_smoke_log": True,
    "burning_rate": 0.75,
    "flame_smoke": 1.0,
    "flame_vorticity": 0.1,
    "flame_ignition": 1.5,
    "flame_max_temp": 3.0,
    "flame_smoke_color": (0.7, 0.7, 0.7),
    "noise_strength": 1.0,
    "noise_pos_scale": 2.0,
    "noise_time_anim": 0.1,
    "noise_scale": 2,
    "use_noise": False,
    "use_mesh": True,
    "cache_frame_start": 1,
    "cache_frame_end": 60,
    "cache_frame_offset": 0,
    "cache_mesh_format": "BOBJECT",
    "cache_data_format": "OPENVDB",
    "cache_noise_format": "OPENVDB",
    "cache_type": "MODULAR",
    "cache_resumable": False,
    "openvdb_data_depth": "16",
    "time_scale": 1.0,
    "use_adaptive_timesteps": True,
    "cfl_condition": 4.0,
    "timesteps_min": 1,
    "timesteps_max": 4,
    "use_slice": False,
    "slice_axis": "AUTO",
    "slice_per_voxel": 5.0,
    "slice_depth": 0.5,
    "display_thickness": 1.0,
    "display_interpolation": "LINEAR",
    "show_gridlines": False,
    "show_velocity": False,
    "vector_display_type": "NEEDLE",
    "vector_field": "FLUID_VELOCITY",
    "vector_scale_with_magnitude": True,
    "vector_show_mac_x": True,
    "vector_show_mac_y": True,
    "vector_show_mac_z": True,
    "vector_scale": 1.0,
    "use_color_ramp": False,
    "color_ramp_field": "DENSITY",
    "color_ramp_field_scale": 1.0,
    "clipping": 0.000001,
    "gridlines_color_field": "NONE",
    "gridlines_lower_bound": 0.0,
    "gridlines_upper_bound": 1.0,
    "gridlines_range_color": (1.0, 0.0, 0.0, 1.0),
    "gridlines_cell_filter": "NONE",
    "velocity_scale": 1.0,
}


FIRE_SMOKE_FLOW_SETTINGS = {
    **FLOW_SETTINGS,
    "flow_type": "BOTH",
    "use_texture": False,
}

FIRE_SMOKE_DOMAIN_SETTINGS = {
    **DOMAIN_SETTINGS,
    "use_adaptive_domain": False,
    "flame_smoke": 0.5,
}


TURBULENCE_SETTINGS = {
    "type": "TURBULENCE",
    "shape": "POINT",
    "falloff_type": "SPHERE",
    "texture_mode": "RGB",
    "z_direction": "BOTH",
    "strength": 0.4,
    "linear_drag": 0.4,
    "harmonic_damping": 1.0,
    "quadratic_drag": 1.0,
    "flow": 0.0,
    "wind_factor": 0.0,
    "inflow": 0.0,
    "size": 0.0,
    "rest_length": 0.0,
    "falloff_power": 0.0,
    "distance_min": 0.0,
    "distance_max": 0.0,
    "radial_min": 0.0,
    "radial_max": 0.0,
    "radial_falloff": 0.0,
    "texture_nabla": 0.0,
    "noise": 0.4,
    "seed": 12,
    "use_min_distance": False,
    "use_max_distance": False,
    "use_radial_min": False,
    "use_radial_max": False,
    "use_object_coords": False,
    "use_global_coords": False,
    "use_2d_force": False,
    "use_root_coords": False,
    "apply_to_location": True,
    "apply_to_rotation": True,
    "use_absorption": False,
    "use_multiple_springs": False,
    "use_smoke_density": False,
    "use_gravity_falloff": False,
    "guide_minimum": 0.4,
    "guide_free": 0.0,
    "use_guide_path_add": False,
    "use_guide_path_weight": False,
    "guide_clump_amount": 0.0,
    "guide_clump_shape": 0.0,
    "guide_kink_type": "NONE",
    "guide_kink_axis": "X",
    "guide_kink_frequency": 0.0,
    "guide_kink_shape": 0.0,
    "guide_kink_amplitude": 0.0,
}


HEAT_STRENGTH_RAMP = (
    (0.6936362981796265, (0.0, 0.0, 0.0, 1.0)),
    (0.9236364364624023, (1.0, 1.0, 1.0, 1.0)),
    (
        1.0,
        (
            0.018809938803315163,
            0.018809938803315163,
            0.018809938803315163,
            1.0,
        ),
    ),
)

HEAT_COLOR_RAMP = (
    (
        0.7018181085586548,
        (1.0, 0.1253650188446045, 0.022117478772997856, 1.0),
    ),
    (
        1.0,
        (1.0, 0.6684743762016296, 0.06056980788707733, 1.0),
    ),
)

NOISE_MASK_RAMP = (
    (0.3963637351989746, (0.0, 0.0, 0.0, 1.0)),
    (1.0, (1.0, 1.0, 1.0, 1.0)),
)

FIRE_SMOKE_HEAT_STRENGTH_RAMP = (
    (0.7163634300231934, (0.0, 0.0, 0.0, 1.0)),
    (0.9236364364624023, (1.0, 1.0, 1.0, 1.0)),
    (
        1.0,
        (
            0.018809938803315163,
            0.018809938803315163,
            0.018809938803315163,
            1.0,
        ),
    ),
)

FIRE_SMOKE_HEAT_COLOR_RAMP = (
    (
        0.0,
        (1.0, 0.6684743762016296, 0.06056980788707733, 1.0),
    ),
    (
        1.0,
        (1.0, 0.7898028492927551, 0.24104410409927368, 1.0),
    ),
)


def set_supported(data, property_name, value):
    if not hasattr(data, property_name):
        return

    try:
        setattr(data, property_name, value)
    except (AttributeError, TypeError, ValueError):
        # Fluid RNA has version- and domain-specific properties.
        pass


def socket_by_identifier(sockets, identifier):
    for socket in sockets:
        if socket.identifier == identifier:
            return socket
    return None


def set_socket(node, identifier, value):
    socket = socket_by_identifier(node.inputs, identifier)
    if socket is not None and hasattr(socket, "default_value"):
        socket.default_value = value


def link_sockets(node_tree, from_node, from_identifier, to_node, to_identifier):
    output_socket = socket_by_identifier(from_node.outputs, from_identifier)
    input_socket = socket_by_identifier(to_node.inputs, to_identifier)
    if output_socket is not None and input_socket is not None:
        node_tree.links.new(output_socket, input_socket)


def configure_color_ramp(node, interpolation, values):
    color_ramp = node.color_ramp
    color_ramp.color_mode = "RGB"
    color_ramp.hue_interpolation = "NEAR"
    color_ramp.interpolation = interpolation

    while len(color_ramp.elements) > 1:
        color_ramp.elements.remove(color_ramp.elements[-1])

    first_position, first_color = values[0]
    first_element = color_ramp.elements[0]
    first_element.position = first_position
    first_element.color = first_color

    for position, color in values[1:]:
        element = color_ramp.elements.new(position)
        element.color = color


def create_flow_texture():
    texture = bpy.data.textures.new(name="纹理", type="CLOUDS")
    texture.use_clamp = True
    texture.use_color_ramp = False
    texture.intensity = 1.0
    texture.contrast = 5.0
    texture.saturation = 1.0
    texture.factor_red = 1.0
    texture.factor_green = 1.0
    texture.factor_blue = 1.0
    texture.use_preview_alpha = False
    texture.noise_scale = 0.1
    texture.noise_depth = 2
    texture.noise_basis = "BLENDER_ORIGINAL"
    texture.noise_type = "SOFT_NOISE"
    texture.cloud_type = "GRAYSCALE"
    texture.nabla = 0.025
    return texture


def configure_flow_modifier(modifier, values, texture=None):
    modifier.name = "流体"
    settings = modifier.flow_settings
    if settings is None:
        raise RuntimeError("无法读取流体源设置")

    for property_name, value in values.items():
        set_supported(settings, property_name, value)
    settings.noise_texture = texture


def configure_domain_modifier(modifier, values, resolution, frame_start, frame_end):
    modifier.name = "流体"
    settings = modifier.domain_settings
    if settings is None:
        raise RuntimeError("无法读取烟雾域设置")

    set_supported(settings, "domain_type", "GAS")
    for property_name, value in values.items():
        set_supported(settings, property_name, value)
    settings.resolution_max = resolution
    settings.cache_frame_start = frame_start
    settings.cache_frame_end = frame_end


def create_domain_material(domain):
    if domain.data.materials:
        material = domain.data.materials[0]
    else:
        material = bpy.data.materials.new(name="烟雾域材质")
        domain.data.materials.append(material)

    material.name = "烟雾域材质"
    material.use_nodes = True
    set_supported(material, "surface_render_method", "DITHERED")
    set_supported(material, "blend_method", "HASHED")
    set_supported(material, "volume_intersection_method", "FAST")

    node_tree = material.node_tree
    node_tree.nodes.clear()

    output = node_tree.nodes.new("ShaderNodeOutputMaterial")
    output.name = "材质输出"
    output.location = (1769.197021484375, 109.2068099975586)
    output.is_active_output = True

    volume = node_tree.nodes.new("ShaderNodeVolumePrincipled")
    volume.name = "原理化体积"
    volume.location = (1369.197265625, 109.2068099975586)
    set_socket(volume, "Density", 0.0)
    set_socket(volume, "Density Attribute", "density")
    set_socket(volume, "Emission Strength", 0.0)
    set_socket(volume, "Temperature Attribute", "temperature")

    heat = node_tree.nodes.new("ShaderNodeAttribute")
    heat.name = "属性"
    heat.location = (195.63119506835938, 33.47623825073242)
    heat.attribute_type = "GEOMETRY"
    heat.attribute_name = "heat"

    strength_ramp = node_tree.nodes.new("ShaderNodeValToRGB")
    strength_ramp.name = "颜色渐变"
    strength_ramp.location = (464.26788330078125, 50.20234298706055)
    configure_color_ramp(strength_ramp, "EASE", HEAT_STRENGTH_RAMP)

    color_ramp = node_tree.nodes.new("ShaderNodeValToRGB")
    color_ramp.name = "颜色渐变.001"
    color_ramp.location = (462.50396728515625, -165.4436798095703)
    configure_color_ramp(color_ramp, "LINEAR", HEAT_COLOR_RAMP)

    strength_multiply = node_tree.nodes.new("ShaderNodeMath")
    strength_multiply.name = "运算"
    strength_multiply.location = (840.2459106445312, 104.12831115722656)
    strength_multiply.operation = "MULTIPLY"
    set_socket(strength_multiply, "Value_001", 10.0)

    noise = node_tree.nodes.new("ShaderNodeTexNoise")
    noise.name = "噪波纹理"
    noise.location = (244.9455108642578, 377.2550048828125)
    noise.show_texture = True
    noise.noise_dimensions = "3D"
    set_supported(noise, "noise_type", "FBM")
    set_supported(noise, "normalize", True)
    set_socket(noise, "Scale", 8.0)
    set_socket(noise, "Detail", 9.4)
    set_socket(noise, "Roughness", 0.5)
    set_socket(noise, "Lacunarity", 2.0)
    set_socket(noise, "Distortion", 1.0)

    noise_ramp = node_tree.nodes.new("ShaderNodeValToRGB")
    noise_ramp.name = "颜色渐变.002"
    noise_ramp.location = (481.79010009765625, 378.6423034667969)
    configure_color_ramp(noise_ramp, "LINEAR", NOISE_MASK_RAMP)

    emission_multiply = node_tree.nodes.new("ShaderNodeMath")
    emission_multiply.name = "运算.001"
    emission_multiply.location = (1105.5341796875, 96.35960388183594)
    emission_multiply.operation = "MULTIPLY"
    set_socket(emission_multiply, "Value_001", 10.0)

    link_sockets(node_tree, volume, "Volume", output, "Volume")
    link_sockets(node_tree, heat, "Fac", strength_ramp, "Fac")
    link_sockets(node_tree, emission_multiply, "Value", volume, "Emission Strength")
    link_sockets(node_tree, heat, "Fac", color_ramp, "Fac")
    link_sockets(node_tree, color_ramp, "Color", volume, "Emission Color")
    link_sockets(node_tree, strength_ramp, "Color", strength_multiply, "Value")
    link_sockets(
        node_tree,
        strength_multiply,
        "Value",
        emission_multiply,
        "Value",
    )
    link_sockets(node_tree, noise, "Fac", noise_ramp, "Fac")
    link_sockets(
        node_tree,
        noise_ramp,
        "Color",
        strength_multiply,
        "Value_001",
    )

    return material


def create_fire_smoke_domain_material(domain):
    if domain.data.materials:
        material = domain.data.materials[0]
    else:
        material = bpy.data.materials.new(name="烟雾域材质")
        domain.data.materials.append(material)

    material.name = "烟雾域材质"
    material.use_nodes = True
    set_supported(material, "surface_render_method", "DITHERED")
    set_supported(material, "blend_method", "HASHED")
    set_supported(material, "volume_intersection_method", "FAST")

    node_tree = material.node_tree
    node_tree.nodes.clear()

    output = node_tree.nodes.new("ShaderNodeOutputMaterial")
    output.name = "材质输出"
    output.location = (1200.0, 150.0)
    output.is_active_output = True

    volume = node_tree.nodes.new("ShaderNodeVolumePrincipled")
    volume.name = "原理化体积"
    volume.location = (800.0, 150.0)
    set_socket(volume, "Density", 5.0)
    set_socket(volume, "Density Attribute", "density")
    set_socket(volume, "Emission Strength", 0.0)
    set_socket(volume, "Temperature Attribute", "temperature")

    heat = node_tree.nodes.new("ShaderNodeAttribute")
    heat.name = "属性"
    heat.location = (-493.3782653808594, 20.256763458251953)
    heat.attribute_type = "GEOMETRY"
    heat.attribute_name = "heat"

    strength_ramp = node_tree.nodes.new("ShaderNodeValToRGB")
    strength_ramp.name = "颜色渐变"
    strength_ramp.location = (-224.7415771484375, 36.98286819458008)
    configure_color_ramp(
        strength_ramp,
        "EASE",
        FIRE_SMOKE_HEAT_STRENGTH_RAMP,
    )

    color_ramp = node_tree.nodes.new("ShaderNodeValToRGB")
    color_ramp.name = "颜色渐变.001"
    color_ramp.location = (-226.5054931640625, -178.66314697265625)
    configure_color_ramp(
        color_ramp,
        "LINEAR",
        FIRE_SMOKE_HEAT_COLOR_RAMP,
    )

    strength_multiply = node_tree.nodes.new("ShaderNodeMath")
    strength_multiply.name = "运算"
    strength_multiply.location = (151.2364501953125, 90.9088363647461)
    strength_multiply.operation = "MULTIPLY"
    set_socket(strength_multiply, "Value_001", 10.0)

    noise = node_tree.nodes.new("ShaderNodeTexNoise")
    noise.name = "噪波纹理"
    noise.location = (-444.06396484375, 364.0355224609375)
    noise.show_texture = True
    noise.noise_dimensions = "3D"
    set_supported(noise, "noise_type", "FBM")
    set_supported(noise, "normalize", True)
    set_socket(noise, "Scale", 8.0)
    set_socket(noise, "Detail", 9.4)
    set_socket(noise, "Roughness", 0.5)
    set_socket(noise, "Lacunarity", 2.0)
    set_socket(noise, "Distortion", 1.0)

    noise_ramp = node_tree.nodes.new("ShaderNodeValToRGB")
    noise_ramp.name = "颜色渐变.002"
    noise_ramp.location = (-207.2193603515625, 365.4228210449219)
    configure_color_ramp(noise_ramp, "LINEAR", NOISE_MASK_RAMP)

    blackbody_multiply = node_tree.nodes.new("ShaderNodeMath")
    blackbody_multiply.name = "运算.001"
    blackbody_multiply.location = (416.52471923828125, 83.14012908935547)
    blackbody_multiply.operation = "MULTIPLY"
    set_socket(blackbody_multiply, "Value_001", 25.0)

    link_sockets(node_tree, volume, "Volume", output, "Volume")
    link_sockets(node_tree, heat, "Fac", strength_ramp, "Fac")
    link_sockets(node_tree, heat, "Fac", color_ramp, "Fac")
    link_sockets(node_tree, strength_ramp, "Color", strength_multiply, "Value")
    link_sockets(
        node_tree,
        strength_multiply,
        "Value",
        blackbody_multiply,
        "Value",
    )
    link_sockets(node_tree, noise, "Fac", noise_ramp, "Fac")
    link_sockets(
        node_tree,
        noise_ramp,
        "Color",
        strength_multiply,
        "Value_001",
    )
    link_sockets(
        node_tree,
        blackbody_multiply,
        "Value",
        volume,
        "Blackbody Intensity",
    )
    link_sockets(
        node_tree,
        color_ramp,
        "Color",
        volume,
        "Blackbody Tint",
    )

    return material


def create_turbulence(source, height_offset):
    source_location = source.matrix_world.translation
    location = (
        source_location.x,
        source_location.y,
        source_location.z + height_offset,
    )
    bpy.ops.object.effector_add(type="TURBULENCE", location=location)
    turbulence = bpy.context.object
    turbulence.name = "紊流"

    collection = (
        source.users_collection[0]
        if source.users_collection
        else bpy.context.scene.collection
    )
    if turbulence.name not in collection.objects:
        collection.objects.link(turbulence)
        for current_collection in list(turbulence.users_collection):
            if current_collection != collection:
                current_collection.objects.unlink(turbulence)

    turbulence.empty_display_type = "PLAIN_AXES"
    turbulence.empty_display_size = 1.0

    for property_name, value in TURBULENCE_SETTINGS.items():
        set_supported(turbulence.field, property_name, value)

    return turbulence


def find_fluid_modifier(obj, fluid_type):
    for modifier in obj.modifiers:
        if modifier.type == "FLUID" and modifier.fluid_type == fluid_type:
            return modifier
    return None


def restore_selection(context, selected_objects, active_object):
    bpy.ops.object.select_all(action="DESELECT")
    for obj in selected_objects:
        if obj.name in context.view_layer.objects:
            obj.select_set(True)
    if active_object and active_object.name in context.view_layer.objects:
        context.view_layer.objects.active = active_object


def can_add_reference_effect(context):
    return (
        context.mode == "OBJECT"
        and any(obj.type == "MESH" for obj in context.selected_objects)
    )


def add_reference_effect(
    operator,
    context,
    *,
    quick_smoke_style,
    flow_values,
    domain_values,
    material_builder,
    turbulence_height,
    effect_name,
):
    scene = context.scene
    if scene.reference_fire_frame_end < scene.reference_fire_frame_start:
        operator.report({"ERROR"}, "结束帧不能小于开始帧")
        return {"CANCELLED"}

    flow_objects = [
        obj
        for obj in context.selected_objects
        if obj.type == "MESH" and find_fluid_modifier(obj, "DOMAIN") is None
    ]
    if not flow_objects:
        operator.report({"ERROR"}, "请至少选择一个网格物体")
        return {"CANCELLED"}

    objects_with_flow = [
        obj for obj in flow_objects if find_fluid_modifier(obj, "FLOW")
    ]
    if objects_with_flow:
        names = "、".join(obj.name for obj in objects_with_flow[:3])
        operator.report({"ERROR"}, f"以下物体已有流体源，未重复添加：{names}")
        return {"CANCELLED"}

    original_selection = list(context.selected_objects)
    original_active = context.view_layer.objects.active
    objects_before = set(context.scene.objects)

    bpy.ops.object.select_all(action="DESELECT")
    for obj in flow_objects:
        obj.select_set(True)
    context.view_layer.objects.active = flow_objects[0]

    try:
        result = bpy.ops.object.quick_smoke(
            style=quick_smoke_style,
            show_flows=False,
        )
    except RuntimeError as error:
        restore_selection(context, original_selection, original_active)
        operator.report({"ERROR"}, f"快速烟雾创建失败：{error}")
        return {"CANCELLED"}

    if "FINISHED" not in result:
        restore_selection(context, original_selection, original_active)
        operator.report({"ERROR"}, "快速烟雾创建失败")
        return {"CANCELLED"}

    new_objects = [
        obj for obj in context.scene.objects if obj not in objects_before
    ]
    domain = next(
        (
            obj
            for obj in new_objects
            if find_fluid_modifier(obj, "DOMAIN") is not None
        ),
        None,
    )
    if domain is None:
        operator.report({"ERROR"}, "未找到快速烟雾生成的烟雾域")
        return {"CANCELLED"}

    try:
        texture = create_flow_texture() if flow_values["use_texture"] else None
        for obj in flow_objects:
            configure_flow_modifier(
                find_fluid_modifier(obj, "FLOW"),
                flow_values,
                texture,
            )
            create_turbulence(obj, turbulence_height)

        domain.name = "烟雾域"
        domain.display_type = "WIRE"
        configure_domain_modifier(
            find_fluid_modifier(domain, "DOMAIN"),
            domain_values,
            scene.reference_fire_resolution,
            scene.reference_fire_frame_start,
            scene.reference_fire_frame_end,
        )
        material_builder(domain)
    except (AttributeError, RuntimeError, TypeError, ValueError) as error:
        operator.report({"ERROR"}, f"参考参数应用失败：{error}")
        return {"CANCELLED"}

    scene.reference_fire_last_domain = domain
    bpy.ops.object.select_all(action="DESELECT")
    domain.select_set(True)
    context.view_layer.objects.active = domain
    operator.report(
        {"INFO"},
        f"已为 {len(flow_objects)} 个物体创建{effect_name}和紊流",
    )
    return {"FINISHED"}


class OBJECT_OT_add_reference_fire(bpy.types.Operator):
    bl_idname = "object.add_reference_fire"
    bl_label = "添加火焰燃烧效果"
    bl_description = "按球体和烟雾域的参考参数创建火焰、烟雾域与紊流"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return can_add_reference_effect(context)

    def execute(self, context):
        return add_reference_effect(
            self,
            context,
            quick_smoke_style="FIRE",
            flow_values=FLOW_SETTINGS,
            domain_values=DOMAIN_SETTINGS,
            material_builder=create_domain_material,
            turbulence_height=2.1953630447387695,
            effect_name="火焰燃烧效果",
        )


class OBJECT_OT_add_reference_fire_smoke(bpy.types.Operator):
    bl_idname = "object.add_reference_fire_smoke"
    bl_label = "添加火焰与烟雾效果"
    bl_description = "按球体.001和烟雾域.001的参考参数创建火焰烟雾与紊流"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return can_add_reference_effect(context)

    def execute(self, context):
        return add_reference_effect(
            self,
            context,
            quick_smoke_style="BOTH",
            flow_values=FIRE_SMOKE_FLOW_SETTINGS,
            domain_values=FIRE_SMOKE_DOMAIN_SETTINGS,
            material_builder=create_fire_smoke_domain_material,
            turbulence_height=2.276984214782715,
            effect_name="火焰与烟雾效果",
        )


def find_bake_domain(context):
    domain = context.scene.reference_fire_last_domain
    if (
        domain is not None
        and domain.name in context.scene.objects
        and find_fluid_modifier(domain, "DOMAIN") is not None
    ):
        return domain

    active = context.view_layer.objects.active
    if active is not None and find_fluid_modifier(active, "DOMAIN") is not None:
        return active

    for obj in reversed(list(context.scene.objects)):
        if find_fluid_modifier(obj, "DOMAIN") is not None:
            return obj
    return None


class OBJECT_OT_bake_reference_fire_data(bpy.types.Operator):
    bl_idname = "object.bake_reference_fire_data"
    bl_label = "烘焙数据"
    bl_description = "烘焙插件最近生成的烟雾域流体数据"

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        domain = find_bake_domain(context)
        if domain is None:
            self.report({"ERROR"}, "未找到可烘焙的烟雾域")
            return {"CANCELLED"}

        modifier = find_fluid_modifier(domain, "DOMAIN")
        settings = modifier.domain_settings
        if settings is None:
            self.report({"ERROR"}, "无法读取烟雾域设置")
            return {"CANCELLED"}
        if settings.has_cache_baked_data:
            self.report({"INFO"}, "该烟雾域的数据已经烘焙")
            return {"CANCELLED"}
        if settings.is_cache_baking_data:
            self.report({"INFO"}, "该烟雾域正在烘焙数据")
            return {"CANCELLED"}

        bpy.ops.object.select_all(action="DESELECT")
        domain.select_set(True)
        context.view_layer.objects.active = domain

        try:
            result = bpy.ops.fluid.bake_data()
        except RuntimeError as error:
            self.report({"ERROR"}, f"烘焙数据失败：{error}")
            return {"CANCELLED"}

        if "FINISHED" not in result:
            self.report({"ERROR"}, "Blender 未能启动流体数据烘焙")
            return {"CANCELLED"}

        self.report({"INFO"}, f"已完成烟雾域数据烘焙：{domain.name}")
        return {"FINISHED"}


class VIEW3D_PT_reference_fire(bpy.types.Panel):
    bl_label = "参考火焰燃烧"
    bl_idname = "VIEW3D_PT_reference_fire"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "火焰"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.label(text="选择一个或多个网格物体")
        layout.operator(
            OBJECT_OT_add_reference_fire.bl_idname,
            icon="MOD_FLUIDSIM",
        )
        layout.operator(
            OBJECT_OT_add_reference_fire_smoke.bl_idname,
            icon="MOD_FLUIDSIM",
        )
        layout.separator()
        layout.prop(scene, "reference_fire_resolution")

        row = layout.row(align=True)
        row.prop(scene, "reference_fire_frame_start", text="开始帧")
        row.prop(scene, "reference_fire_frame_end", text="结束帧")

        layout.separator()
        layout.operator(
            OBJECT_OT_bake_reference_fire_data.bl_idname,
            icon="REC",
        )


def draw_quick_effect_menu(self, _context):
    self.layout.operator(
        OBJECT_OT_add_reference_fire.bl_idname,
        icon="MOD_FLUIDSIM",
    )
    self.layout.operator(
        OBJECT_OT_add_reference_fire_smoke.bl_idname,
        icon="MOD_FLUIDSIM",
    )


CLASSES = (
    OBJECT_OT_add_reference_fire,
    OBJECT_OT_add_reference_fire_smoke,
    OBJECT_OT_bake_reference_fire_data,
    VIEW3D_PT_reference_fire,
)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    bpy.types.Scene.reference_fire_resolution = bpy.props.IntProperty(
        name="域分辨率",
        description="烟雾域最大分辨率",
        default=256,
        min=6,
        soft_max=1024,
    )
    bpy.types.Scene.reference_fire_frame_start = bpy.props.IntProperty(
        name="开始帧",
        description="流体缓存开始帧",
        default=1,
        min=1,
    )
    bpy.types.Scene.reference_fire_frame_end = bpy.props.IntProperty(
        name="结束帧",
        description="流体缓存结束帧",
        default=60,
        min=1,
    )
    bpy.types.Scene.reference_fire_last_domain = bpy.props.PointerProperty(
        name="最近生成的烟雾域",
        type=bpy.types.Object,
    )
    bpy.types.VIEW3D_MT_object_quick_effects.append(draw_quick_effect_menu)


def unregister():
    bpy.types.VIEW3D_MT_object_quick_effects.remove(draw_quick_effect_menu)
    del bpy.types.Scene.reference_fire_last_domain
    del bpy.types.Scene.reference_fire_frame_end
    del bpy.types.Scene.reference_fire_frame_start
    del bpy.types.Scene.reference_fire_resolution
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
