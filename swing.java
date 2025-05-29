import javax.swing.*;
import java.awt.*;

public class swing {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame f = new JFrame("JLabelDemo");
            f.setLayout(new FlowLayout());
            f.setSize(260, 210);
            f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

            JLabel label = new JLabel("Hourglass", new ImageIcon("hourglass.png"), JLabel.CENTER);
            JButton jb = new JButton("Button", new ImageIcon("hourglass.png"));
            JLabel label1 = new JLabel("Hourg", new ImageIcon("hourglass.png"), JLabel.LEADING);
            
            JLabel label2 = new JLabel("h", new ImageIcon("hourglass.png"), JLabel.RIGHT);

            jb.addActionListener(e -> label.setText("hourglass"));

            f.add(label);
            f.add(label2);
            f.add(label1);
            f.add(jb);

            f.setVisible(true);
        });
    }
}