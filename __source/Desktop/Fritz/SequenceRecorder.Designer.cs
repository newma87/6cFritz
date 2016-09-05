namespace Fritz
{
    partial class SequenceRecorder
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
          this.components = new System.ComponentModel.Container();
          System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(SequenceRecorder));
          this.recordBtn = new System.Windows.Forms.Button();
          this.stopBtn = new System.Windows.Forms.Button();
          this.pauseBtn = new System.Windows.Forms.Button();
          this.label6 = new System.Windows.Forms.Label();
          this.sensitivity = new System.Windows.Forms.ComboBox();
          this.audioLevel = new System.Windows.Forms.ProgressBar();
          this.label2 = new System.Windows.Forms.Label();
          this.microphoneList = new System.Windows.Forms.ComboBox();
          this.label1 = new System.Windows.Forms.Label();
          this.buttonOK = new System.Windows.Forms.Button();
          this.buttonCancel = new System.Windows.Forms.Button();
          this.label3 = new System.Windows.Forms.Label();
          this.timer2 = new System.Windows.Forms.Timer(this.components);
          this.audioCheckbox = new System.Windows.Forms.CheckBox();
          this.joystickCheckbox = new System.Windows.Forms.CheckBox();
          this.keyboardCheckBox = new System.Windows.Forms.CheckBox();
          this.SuspendLayout();
          // 
          // recordBtn
          // 
          this.recordBtn.Image = ((System.Drawing.Image)(resources.GetObject("recordBtn.Image")));
          this.recordBtn.Location = new System.Drawing.Point(66, 193);
          this.recordBtn.Name = "recordBtn";
          this.recordBtn.Size = new System.Drawing.Size(56, 36);
          this.recordBtn.TabIndex = 0;
          this.recordBtn.UseVisualStyleBackColor = true;
          this.recordBtn.Click += new System.EventHandler(this.recordBtn_Click);
          // 
          // stopBtn
          // 
          this.stopBtn.Enabled = false;
          this.stopBtn.Image = ((System.Drawing.Image)(resources.GetObject("stopBtn.Image")));
          this.stopBtn.Location = new System.Drawing.Point(128, 193);
          this.stopBtn.Name = "stopBtn";
          this.stopBtn.Size = new System.Drawing.Size(56, 36);
          this.stopBtn.TabIndex = 1;
          this.stopBtn.UseVisualStyleBackColor = true;
          this.stopBtn.Click += new System.EventHandler(this.stopBtn_Click);
          // 
          // pauseBtn
          // 
          this.pauseBtn.Enabled = false;
          this.pauseBtn.Image = ((System.Drawing.Image)(resources.GetObject("pauseBtn.Image")));
          this.pauseBtn.Location = new System.Drawing.Point(190, 193);
          this.pauseBtn.Name = "pauseBtn";
          this.pauseBtn.Size = new System.Drawing.Size(56, 36);
          this.pauseBtn.TabIndex = 2;
          this.pauseBtn.UseVisualStyleBackColor = true;
          this.pauseBtn.Click += new System.EventHandler(this.pauseBtn_Click);
          // 
          // label6
          // 
          this.label6.AutoSize = true;
          this.label6.Location = new System.Drawing.Point(9, 106);
          this.label6.Name = "label6";
          this.label6.Size = new System.Drawing.Size(63, 13);
          this.label6.TabIndex = 76;
          this.label6.Text = "Audio Level";
          // 
          // sensitivity
          // 
          this.sensitivity.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
          this.sensitivity.FormattingEnabled = true;
          this.sensitivity.Items.AddRange(new object[] {
            "1 - low",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7 - high"});
          this.sensitivity.Location = new System.Drawing.Point(128, 155);
          this.sensitivity.Name = "sensitivity";
          this.sensitivity.Size = new System.Drawing.Size(72, 21);
          this.sensitivity.TabIndex = 73;
          // 
          // audioLevel
          // 
          this.audioLevel.Location = new System.Drawing.Point(12, 122);
          this.audioLevel.Name = "audioLevel";
          this.audioLevel.Size = new System.Drawing.Size(264, 23);
          this.audioLevel.TabIndex = 72;
          // 
          // label2
          // 
          this.label2.AutoSize = true;
          this.label2.Location = new System.Drawing.Point(9, 62);
          this.label2.Name = "label2";
          this.label2.Size = new System.Drawing.Size(85, 13);
          this.label2.TabIndex = 71;
          this.label2.Text = "Use Microphone";
          // 
          // microphoneList
          // 
          this.microphoneList.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
          this.microphoneList.FormattingEnabled = true;
          this.microphoneList.Location = new System.Drawing.Point(12, 80);
          this.microphoneList.Name = "microphoneList";
          this.microphoneList.Size = new System.Drawing.Size(264, 21);
          this.microphoneList.TabIndex = 70;
          // 
          // label1
          // 
          this.label1.AutoSize = true;
          this.label1.Location = new System.Drawing.Point(9, 158);
          this.label1.Name = "label1";
          this.label1.Size = new System.Drawing.Size(113, 13);
          this.label1.TabIndex = 69;
          this.label1.Text = "Microphone Sensitivity";
          // 
          // buttonOK
          // 
          this.buttonOK.DialogResult = System.Windows.Forms.DialogResult.OK;
          this.buttonOK.Location = new System.Drawing.Point(120, 244);
          this.buttonOK.Name = "buttonOK";
          this.buttonOK.Size = new System.Drawing.Size(75, 23);
          this.buttonOK.TabIndex = 78;
          this.buttonOK.Text = "OK";
          this.buttonOK.UseVisualStyleBackColor = true;
          this.buttonOK.Click += new System.EventHandler(this.buttonOK_Click);
          // 
          // buttonCancel
          // 
          this.buttonCancel.DialogResult = System.Windows.Forms.DialogResult.Cancel;
          this.buttonCancel.Location = new System.Drawing.Point(201, 244);
          this.buttonCancel.Name = "buttonCancel";
          this.buttonCancel.Size = new System.Drawing.Size(75, 23);
          this.buttonCancel.TabIndex = 77;
          this.buttonCancel.Text = "Cancel";
          this.buttonCancel.UseVisualStyleBackColor = true;
          this.buttonCancel.Click += new System.EventHandler(this.buttonCancel_Click);
          // 
          // label3
          // 
          this.label3.AutoSize = true;
          this.label3.Location = new System.Drawing.Point(11, 9);
          this.label3.Name = "label3";
          this.label3.Size = new System.Drawing.Size(118, 13);
          this.label3.TabIndex = 79;
          this.label3.Text = "Record into sequencer.";
          // 
          // audioCheckbox
          // 
          this.audioCheckbox.AutoSize = true;
          this.audioCheckbox.Location = new System.Drawing.Point(14, 36);
          this.audioCheckbox.Name = "audioCheckbox";
          this.audioCheckbox.Size = new System.Drawing.Size(53, 17);
          this.audioCheckbox.TabIndex = 80;
          this.audioCheckbox.Text = "Audio";
          this.audioCheckbox.UseVisualStyleBackColor = true;
          this.audioCheckbox.CheckedChanged += new System.EventHandler(this.audioCheckbox_CheckedChanged);
          // 
          // joystickCheckbox
          // 
          this.joystickCheckbox.AutoSize = true;
          this.joystickCheckbox.Location = new System.Drawing.Point(87, 36);
          this.joystickCheckbox.Name = "joystickCheckbox";
          this.joystickCheckbox.Size = new System.Drawing.Size(64, 17);
          this.joystickCheckbox.TabIndex = 81;
          this.joystickCheckbox.Text = "Joystick";
          this.joystickCheckbox.UseVisualStyleBackColor = true;
          // 
          // keyboardCheckBox
          // 
          this.keyboardCheckBox.AutoSize = true;
          this.keyboardCheckBox.Location = new System.Drawing.Point(167, 36);
          this.keyboardCheckBox.Name = "keyboardCheckBox";
          this.keyboardCheckBox.Size = new System.Drawing.Size(71, 17);
          this.keyboardCheckBox.TabIndex = 82;
          this.keyboardCheckBox.Text = "Keyboard";
          this.keyboardCheckBox.UseVisualStyleBackColor = true;
          // 
          // SequenceRecorder
          // 
          this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
          this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
          this.ClientSize = new System.Drawing.Size(286, 280);
          this.Controls.Add(this.keyboardCheckBox);
          this.Controls.Add(this.joystickCheckbox);
          this.Controls.Add(this.audioCheckbox);
          this.Controls.Add(this.label3);
          this.Controls.Add(this.buttonOK);
          this.Controls.Add(this.buttonCancel);
          this.Controls.Add(this.label6);
          this.Controls.Add(this.sensitivity);
          this.Controls.Add(this.audioLevel);
          this.Controls.Add(this.label2);
          this.Controls.Add(this.microphoneList);
          this.Controls.Add(this.label1);
          this.Controls.Add(this.pauseBtn);
          this.Controls.Add(this.stopBtn);
          this.Controls.Add(this.recordBtn);
          this.KeyPreview = true;
          this.Name = "SequenceRecorder";
          this.Text = "Sequence Recorder";
          this.KeyDown += new System.Windows.Forms.KeyEventHandler(this.SequenceRecorder_KeyDown);
          this.KeyUp += new System.Windows.Forms.KeyEventHandler(this.SequenceRecorder_KeyUp);
          this.ResumeLayout(false);
          this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button recordBtn;
        private System.Windows.Forms.Button stopBtn;
        private System.Windows.Forms.Button pauseBtn;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.ComboBox sensitivity;
        private System.Windows.Forms.ProgressBar audioLevel;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.ComboBox microphoneList;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button buttonOK;
        private System.Windows.Forms.Button buttonCancel;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Timer timer2;
        private System.Windows.Forms.CheckBox audioCheckbox;
        private System.Windows.Forms.CheckBox joystickCheckbox;
        private System.Windows.Forms.CheckBox keyboardCheckBox;
    }
}