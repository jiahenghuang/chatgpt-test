import gradio as gr
import openai
from merge_algo import merge
from clean import clean

openai.api_key = "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"

examples = [
    ["""备受社会关注的湖南常德滴滴司机遇害案，将于1月3日9时许，在汉寿县人民法院开庭审理。此前，犯罪嫌疑人、19岁大学生杨某淇被鉴定为作案时患有抑郁症，为“有限定刑事责任能力”。
新京报此前报道，2019年3月24日凌晨，滴滴司机陈师傅，搭载19岁大学生杨某淇到常南汽车总站附近。坐在后排的杨某淇趁陈某不备，朝陈某连捅数刀致其死亡。事发监控显示，杨某淇杀人后下车离开。随后，杨某淇到公安机关自首，并供述称“因悲观厌世，精神崩溃，无故将司机杀害”。据杨某淇就读学校的工作人员称，他家有四口人，姐姐是聋哑人。
今日上午，田女士告诉新京报记者，明日开庭时间不变，此前已提出刑事附带民事赔偿，但通过与法院的沟通后获知，对方父母已经没有赔偿的意愿。当时按照人身死亡赔偿金计算共计80多万元，那时也想考虑对方家庭的经济状况。
田女士说，她相信法律，对最后的结果也做好心理准备。对方一家从未道歉，此前庭前会议中，对方提出了嫌疑人杨某淇作案时患有抑郁症的辩护意见。另具警方出具的鉴定书显示，嫌疑人作案时有限定刑事责任能力。
新京报记者从陈师傅的家属处获知，陈师傅有两个儿子，大儿子今年18岁，小儿子还不到5岁。“这对我来说是一起悲剧，对我们生活的影响，肯定是很大的”，田女士告诉新京报记者，丈夫遇害后，他们一家的主劳动力没有了，她自己带着两个孩子和两个老人一起过，“生活很艰辛”，她说，“还好有妹妹的陪伴，现在已经好些了。""", 3],
    ]


def clean_text(context):
    corpus = clean(context)
    return corpus

# 清除输入输出
def clear_input():
    return "", "", "", ""

# 预测函数
def custom_predict(context):
    response = openai.ChatCompletion.create(
           model='gpt-3.5-turbo',
           messages=[
           {"role": "user", "content": context}],
    )
    return response.choices[0].message.content.strip()

def picture_predict(context):
    image_resp = openai.Image.create(prompt=context, n=1, size="512x512")
    result=[item.url for item in image_resp.data]
    return result[0]

def audio_transcription(file_path):
    with open(file_path, "rb") as fr:
        transcript = openai.Audio.transcribe("whisper-1", fr)
    return transcript.text

def classify(text):
    '''
    情感分类
    '''
    moderation_resp = openai.Moderation.create(input=text)
    return str(moderation_resp)

# 构建Blocks上下文
with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.TabItem("chatgpt-3.5-turbo聊天机器人"):
            gr.Markdown("使用chatgpt-3.5-turbo进行问答！")
            with gr.Column():    # 列排列
                context = gr.Textbox(label="文本内容：")
            with gr.Row():
                submit = gr.Button("submit")
            with gr.Column():    # 列排列
                answer = gr.Textbox(label="answer")
            # 绑定submit点击函数
            submit.click(fn=custom_predict, inputs=[context], outputs=[answer])
        with gr.TabItem("语音识别"):
            gr.Markdown("使用chatgpt-3.5-turbo进行语音识别！")
            with gr.Column():    # 列排列
                video = gr.Video(label="上传视频")
            with gr.Row():
                submit = gr.Button("submit")
            with gr.Column():    # 列排列
                answer = gr.Textbox(label="answer")
            # 绑定submit点击函数
            submit.click(fn=audio_transcription, inputs=[video], outputs=[answer])
            
        with gr.TabItem("文本色恐暴识别"):
            gr.Markdown('''hate：根据种族，性别，种族，宗教，国籍，性取向，残疾地位或种姓来表达，煽动或促进仇恨的内容，   
                         hate/threatening:令人讨厌的内容，包括暴力或对目标群体的严重伤害。   
                         self-harm：促进，鼓励或描绘自我伤害行为的内容，例如自杀，切割和饮食失调。   
                         sexual：内容旨在引起性兴奋，例如对性活动的描述或促进性服务（不包括性教育和健康）。   
                         sexual/minors：性内容，其中包括一个18岁以下的个人。   
                         violence：促进或荣耀暴力或庆祝他人的苦难或屈辱的内容。   
                         violence/graphic：在极端图形细节中描述死亡，暴力或严重身体伤害的暴力内容。   
                        ''')
            with gr.Column():    # 列排列
                context = gr.Textbox(label="文本内容：")
            with gr.Row():
                submit = gr.Button("submit")
            with gr.Column():    # 列排列
                answer = gr.Textbox(label="answer")
            # 绑定submit点击函数
            submit.click(fn=classify, inputs=[context], outputs=[answer])
        with gr.TabItem("chatgpt-3.5-图像生成"):
            gr.Markdown("使用chatgpt-3.5-turbo进行图像生成！")
            with gr.Column(variant="panel"):
                with gr.Row(variant="compact"):
                    text = gr.Textbox(
                        label="Enter your prompt",
                        show_label=False,
                        max_lines=1,
                        placeholder="Enter your prompt",
                    ).style(
                        container=False,
                    )
                    btn = gr.Button("Generate image").style(full_width=False)

                gallery = gr.Gallery(
                    label="Generated images", show_label=False, elem_id="gallery"
                ).style(grid=[2], height="auto")
            
            btn.click(picture_predict, text, gallery)
        with gr.TabItem("自动分段"):
            gr.Markdown("输入长文本后和threshold，点击submit按钮，可以自动分段，赶快试试吧！")
            with gr.Column():    # 列排列
                context = gr.Textbox(label="文本内容")
                number = gr.Textbox(label="threshold")
            with gr.Row():       # 行排列
                clear = gr.Button("clear")
                submit = gr.Button("submit")
            with gr.Column():    # 列排列
                answer = gr.Textbox(label="answer")
        
            # 绑定submit点击函数
            submit.click(fn=custom_predict, inputs=[context, number], outputs=[answer])
            # 绑定clear点击函数
            clear.click(fn=clear_input, inputs=[], outputs=[context, number, answer])
            gr.Examples(examples, inputs=[context, number])

        with gr.TabItem("从html里面提取正文"):
            gr.Markdown("输入url，输出标题和正文！")
            with gr.Column():    # 列排列
                url = gr.Textbox(label="url")
                
            with gr.Row():       # 行排列
                clear = gr.Button("clear")
                submit = gr.Button("submit")
            with gr.Column():    # 列排列
                title = gr.Textbox(label="标题内容")
                context = gr.Textbox(label="文本内容")
                # answer = gr.Textbox(label="answer")
            # 绑定submit点击函数
            submit.click(fn=clean_text, inputs=[url], outputs=[title, context])
            # 绑定clear点击函数
            clear.click(fn=clear_input, inputs=[], outputs=[url, title, context])
demo.launch(share=True)