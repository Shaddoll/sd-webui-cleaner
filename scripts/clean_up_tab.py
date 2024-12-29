import modules.scripts as scripts
import gradio as gr

from modules.shared import opts,OptionInfo

from modules import script_callbacks
from modules.ui_components import ToolButton, ResizeHandleRow
import modules.generation_parameters_copypaste as parameters_copypaste
from modules.ui_common import save_files

from scripts import lama
from PIL import Image

def on_ui_settings():
    section = ('cleaner', "Cleaner")
    opts.add_option("cleaner_use_gpu", OptionInfo(True, "Is Use GPU", gr.Checkbox, {"interactive": True}, section=section))


def send_to_cleaner(result):
    image = Image.open(result[0]["name"])
    return image

def on_ui_tabs():
    with gr.Blocks() as object_cleaner_tab:
        is_forge_ui = False
        tab_index = gr.State(value=0)
        with ResizeHandleRow(equal_height=False, variant='compact'):
            with gr.Column(variant='compact'):
                with gr.Tabs(elem_id="mode_cleanup"):
                    with gr.TabItem('Clean up', id="clean_up", elem_id="clean_up_tab") as tab_clean_up:
                        try:
                            from modules_forge.forge_canvas.canvas import ForgeCanvas
                            init_img_with_mask = ForgeCanvas(elem_id="cleanup_img2maskimg", height=512, scribble_color=opts.img2img_inpaint_mask_brush_color, scribble_alpha=70)
                            is_forge_ui = True
                        except ModuleNotFoundError:
                            init_img_with_mask = gr.Image(label="Image for clean up with mask", show_label=False, elem_id="cleanup_img2maskimg", source="upload",
                                                  interactive=True, type="pil", tool="sketch", image_mode="RGBA", height=512, brush_color=opts.img2img_inpaint_mask_brush_color)
                    with gr.TabItem('Clean up upload', id="clean_up_upload", elem_id="clean_up_upload_tab") as tab_clean_up_upload:
                        with gr.Column(elem_id=f"cleanup_image_mask"):
                            clean_up_init_img = gr.Image(label="Image for cleanup", show_label=False, source="upload",
                                                     interactive=True, type="pil", elem_id="cleanup_img_inpaint_base", height=256)
                            clean_up_init_mask = gr.Image(
                                label="Mask", source="upload", interactive=True, type="pil", image_mode="RGBA", elem_id="cleanup_img_inpaint_mask", height=256)
            with gr.Column():
                clean_button = gr.Button("Generate", variant="primary")
                result_gallery = gr.Gallery(label='Output', show_label=False, elem_id=f"cleanup_gallery", columns=4, preview=True, height=opts.gallery_height or None, interactive=False, type="pil", object_fit="contain")

                with gr.Row(elem_id=f"image_buttons", elem_classes="image-buttons"):

                    buttons = {
                        'img2img': ToolButton('🖼️', elem_id=f'_send_to_img2img', tooltip="Send image and generation parameters to img2img tab."),
                        'inpaint': ToolButton('🎨️', elem_id=f'_send_to_inpaint', tooltip="Send image and generation parameters to img2img inpaint tab."),
                        'extras': ToolButton('📐', elem_id=f'_send_to_extras', tooltip="Send image and generation parameters to extras tab."),
                        'cleaner': ToolButton('🧹', elem_id=f'_send_to_cleaner', tooltip="Send image and generation parameters to cleaner tab.")
                    }
                    if is_forge_ui:
                        parameters_copypaste.add_paste_fields("cleaner", init_img_with_mask.background, None)
                    else:
                        parameters_copypaste.add_paste_fields("cleaner", init_img_with_mask, None)
                    for paste_tabname, paste_button in buttons.items():
                        parameters_copypaste.register_paste_params_button(parameters_copypaste.ParamBinding(
                            paste_button=paste_button, tabname=paste_tabname, source_tabname=None, source_image_component=result_gallery,
                            paste_field_names=[]
                        ))
        tab_clean_up.select(fn=lambda: 0, inputs=[], outputs=[tab_index])
        tab_clean_up_upload.select(fn=lambda: 1, inputs=[], outputs=[tab_index])

        if is_forge_ui:
            clean_button_click_inputs = [
                tab_index,
                init_img_with_mask.background,
                init_img_with_mask.foreground,
                clean_up_init_img,
                clean_up_init_mask,
            ]
            click_fn = lama.clean_object_button_click_forge
        else:
            clean_button_click_inputs = [
                tab_index,
                init_img_with_mask,
                clean_up_init_img,
                clean_up_init_mask,
            ]
            click_fn = lama.clean_object_button_click

        clean_button.click(
            fn=click_fn,
            inputs=clean_button_click_inputs,
            outputs=[
                result_gallery
            ],
            show_progress=True,
        )
    return (object_cleaner_tab, "Cleaner", "cleaner_tab"),
                                            
script_callbacks.on_ui_tabs(on_ui_tabs)
script_callbacks.on_ui_settings(on_ui_settings)

