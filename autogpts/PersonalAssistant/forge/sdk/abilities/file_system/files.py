from typing import List
from ..registry import ability
import requests
from typing import List, Tuple

@ability(
    name="list_files",
    description="List files in a directory",
    parameters=[
        {
            "name": "path",
            "description": "Path to the directory",
            "type": "string",
            "required": True,
        }
    ],
    output_type="list[str]",
)
async def list_files(agent, task_id: str, path: str) -> List[str]:
    """
    List files in a workspace directory
    """
    return agent.workspace.list(task_id=task_id, path=path)


@ability(
    name="write_file",
    description="Write data to a file",
    parameters=[
        {
            "name": "file_path",
            "description": "Path to the file",
            "type": "string",
            "required": True,
        },
        {
            "name": "data",
            "description": "Data to write to the file",
            "type": "bytes",
            "required": True,
        },
    ],
    output_type="None",
)
async def write_file(agent, task_id: str, file_path: str, data: bytes) -> None:
    """
    Write data to a file
    """
    if isinstance(data, str):
        data = data.encode()

    agent.workspace.write(task_id=task_id, path=file_path, data=data)
    await agent.db.create_artifact(
        task_id=task_id,
        file_name=file_path.split("/")[-1],
        relative_path=file_path,
        agent_created=True,
    )

@ability(
    name="read_file",
    description="Read data from a file",
    parameters=[
        {
            "name": "file_path",
            "description": "Path to the file",
            "type": "string",
            "required": True,
        },
    ],
    output_type="bytes",
)
async def read_file(agent, task_id: str, file_path: str) -> bytes:
    """
    Read data from a file
    """
    read_text = agent.workspace.read(task_id=task_id, path=file_path)
    agent.workspace.write(task_id=task_id, path="/output.txt", data=read_text)
    await agent.db.create_artifact(
        task_id=task_id,
        file_name='output.txt',
        relative_path='/output.txt',
        agent_created=True,
    )
    print("Testing",file_path)
    return read_text

@ability(
  name="fetch_webpage",
  description="Retrieve the content of a webpage",
  parameters=[
      {
          "name": "url",
          "description": "Webpage URL",
          "type": "string",
          "required": True,
      }
  ],
  output_type="string",
)
async def fetch_webpage(agent, task_id: str, url: str) -> str:
  response = requests.get(url)
  return response.text

@ability(
    name="three_sum",
    description="Finds three integers in an array that add up to a specific target",
    parameters=[
        {
            "name": "array",
            "description": "List of integers",
            "type": "list[int]",
            "required": True,
        },
        {
            "name": "target",
            "description": "Target sum value",
            "type": "int",
            "required": True,
        },
    ],
    output_type="list[tuple[int, int, int]]",
)
async def three_sum(agent, task_id: str, array: List[int], target: int) -> List[Tuple[int, int, int]]:
    """
    Solve the three_sum problem
    """
    array.sort()
    result = []

    for i in range(len(array)):
        left, right = i + 1, len(array) - 1
        while left < right:
            curr_sum = array[i] + array[left] + array[right]
            if curr_sum == target:
                result.append((array[i], array[left], array[right]))
                left += 1
                right -= 1
            elif curr_sum < target:
                left += 1
            else:
                right -= 1

    # Return unique results
    return list(set(result))
