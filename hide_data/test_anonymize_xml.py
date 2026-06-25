from pathlib import Path

from hide_data.anonymize_xml import anonymize_xml


def test_anonymize_xml_masks_selected_tags(tmp_path: Path) -> None:
    source = tmp_path / "input.xml"
    target = tmp_path / "output.xml"

    source.write_text(
        """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<Root>
  <Record>
    <Name>Maria Lopez</Name>
    <Email>maria@example.com</Email>
    <City>Madrid</City>
  </Record>
</Root>
""",
        encoding="utf-8",
    )

    stats = anonymize_xml(
        input_path=source,
        output_path=target,
        tags_to_mask={"Name", "Email"},
        mask_char="X",
    )

    output = target.read_text(encoding="utf-8")
    assert "<Name>XXXXX XXXXX</Name>" in output
    assert "<Email>XXXXX@XXXXXXX.XXX</Email>" in output
    assert "<City>Madrid</City>" in output
    assert stats.elements_masked == 2
    assert stats.text_nodes_masked >= 2
