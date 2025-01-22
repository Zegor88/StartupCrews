from idea_generation_crew.interface import iface

if __name__ == "__main__":
    iface.launch(
        server_name="0.0.0.0", 
        server_port=7860,
        share=True
    )