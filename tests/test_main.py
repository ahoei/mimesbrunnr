from mimesbrunnr import main


def test_main(capsys: object) -> None:
	main()
	captured = capsys.readouterr()
	assert "Hello Mime!" in captured.out
